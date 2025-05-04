import librosa
import numpy as np


import sounddevice as sd
from scipy.spatial.distance import cosine
import os
import time
import threading
from pynput import keyboard, mouse

# === Keyboard/Mouse Action Functions ===
kb_controller = keyboard.Controller()
mouse_controller = mouse.Controller()
delay = 0.05 # Small delay between actions

def perform_initial_setup():
    """Performs the one-time setup actions (Cmd+L, Ctrl+Cmd+T, mouse)."""
    print("⚙️ Performing initial setup actions...")

    print("  > Sending Cmd + L...")
    kb_controller.press(keyboard.Key.cmd)
    time.sleep(delay)
    kb_controller.press('l')
    time.sleep(delay)
    kb_controller.release('l')
    time.sleep(delay)
    kb_controller.release(keyboard.Key.cmd)

    print("  > Waiting 0.5s...")
    time.sleep(0.5)

    print("  > Sending Ctrl + Cmd + T...")
    kb_controller.press(keyboard.Key.ctrl)
    time.sleep(delay)
    kb_controller.press(keyboard.Key.cmd)
    time.sleep(delay)
    kb_controller.press('t')
    time.sleep(delay)
    kb_controller.release('t')
    time.sleep(delay)
    kb_controller.release(keyboard.Key.cmd)
    time.sleep(delay)
    kb_controller.release(keyboard.Key.ctrl)
    time.sleep(delay * 2)

    print("  > Moving mouse to (1400, 150)...")
    mouse_controller.position = (1400, 150)
    time.sleep(delay * 2)

    print("  > Clicking mouse...")
    mouse_controller.click(mouse.Button.left, 1)
    time.sleep(delay * 2)

    print("✅ Initial setup complete!")

def type_hello_world_and_enter():
    """Types 'hello world' and presses Enter."""
    print("⚙️ Typing 'hello world' and pressing Enter...")
    kb_controller.type('hello world')
    time.sleep(delay * 2)
    kb_controller.press(keyboard.Key.enter)
    time.sleep(delay)
    kb_controller.release(keyboard.Key.enter)
    print("✅ Typed and entered!")

# === Step 1: Load the reference sound ===
print("🔍 Loading reference sound...")
reference_fp = None
REFERENCE_SOUND_PATH = os.getenv("REFERENCE_SOUND_PATH", "sample.mp3") # Default to sample.mp3 if not set
# Event to signal sound detection
sound_detected_event = threading.Event()

def load_reference(path):
    if not os.path.exists(path):
        print(f"❌ Error: Reference sound file not found at {path}")
        print("Please ensure the sound file exists or set the REFERENCE_SOUND_PATH environment variable.")
        exit(1)
    try:
        y, sr = librosa.load(path, sr=22050)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        return np.mean(mfcc, axis=1)
    except Exception as e:
        print(f"❌ Error loading reference sound: {e}")
        exit(1)

reference_fp = load_reference(REFERENCE_SOUND_PATH)
print(f"✅ Reference sound loaded from {REFERENCE_SOUND_PATH}.")

# === Step 2: Define thresholds ===
# Similarity threshold (how similar the sound fingerprint must be)
# Try values between 0.8 and 0.98. Lower values are more lenient, higher values are stricter.
MATCH_THRESHOLD = float(os.getenv("MATCH_THRESHOLD", 0.9))
# Loudness threshold (how loud the sound must be in dB)
# Typical values might range from -40 (quieter) to -10 (louder).
# Adjust based on your microphone sensitivity and environment.
LOUDNESS_THRESHOLD_DB = float(os.getenv("LOUDNESS_THRESHOLD_DB", -35.0))
print(f"ℹ️ Using match threshold: {MATCH_THRESHOLD}")
print(f"ℹ️ Using loudness threshold (dB): {LOUDNESS_THRESHOLD_DB}")


# === Step 3: Audio stream parameters ===
SAMPLE_RATE = 22050
# How often the script checks the audio (in seconds). Shorter durations are more responsive but use more CPU.
CHUNK_DURATION = float(os.getenv("CHUNK_DURATION", 1.0))
BLOCKSIZE = int(SAMPLE_RATE * CHUNK_DURATION)

# === Step 4: Callback function for live microphone listening ===
def on_audio(indata, frames, time, status):
    if status:
        print(f"⚠️ Audio stream status: {status}")
    global reference_fp
    # Use only the first channel (mono)
    y = indata[:, 0]

    # --- Calculate Loudness (dB) --- 
    rms = np.sqrt(np.mean(y**2))
    # Avoid log(0) errors; add a small epsilon or check if rms is zero
    if rms > 0:
        decibels = 20 * np.log10(rms)
    else:
        decibels = -np.inf # Or some very small number

    # --- Calculate MFCC Features --- 
    mfcc = librosa.feature.mfcc(y=y, sr=SAMPLE_RATE, n_mfcc=13)
    current_fp = np.mean(mfcc, axis=1)

    # --- Compare Fingerprints --- 
    similarity = 1 - cosine(current_fp, reference_fp)

    # Optional: Print scores for debugging/tuning
    # print(f"Similarity: {similarity:.2f}, Loudness: {decibels:.1f} dB")

    # --- Check both thresholds --- 
    if similarity > MATCH_THRESHOLD and decibels > LOUDNESS_THRESHOLD_DB:
        # --- ACTION TO TAKE ON MATCH --- 
        print("🔊 Match detected!")
        sound_detected_event.set() # Signal the main loop
        # Optional: Stop the stream immediately upon match
        # raise sd.CallbackStop

# === Step 5: Main loop ===
try:
    # --- Perform Initial Setup Actions ONCE ---
    perform_initial_setup()
    print("-"*30)
    # --- First time: Type hello world immediately after setup ---
    type_hello_world_and_enter()
    print("-"*30)

    while True:
        # --- Listen for Sound ---
        sound_detected_event.clear() # Reset the event for the next listen cycle
        print(f"🎧 Listening for target sound (chunk duration: {CHUNK_DURATION}s)... (Ctrl+C to stop)")
        with sd.InputStream(callback=on_audio,
                            channels=1,
                            samplerate=SAMPLE_RATE,
                            blocksize=BLOCKSIZE,
                            dtype='float32'):
            # Wait here until the on_audio callback calls sound_detected_event.set()
            triggered = sound_detected_event.wait() # This blocks execution
            if triggered:
                print("👂 Event triggered, performing action...")
                # --- Perform Repetitive Action ---
                type_hello_world_and_enter()
                print("-"*30)
            # The 'with' block ensures the stream is closed here before looping

except KeyboardInterrupt:
    print("🛑 Stopping listening.")
except Exception as e:
    print(f"❌ An error occurred: {e}")
    if "Invalid number of channels" in str(e):
        print("💡 Tip: Your microphone might not support mono (1 channel). Try setting channels=2 in sd.InputStream.")
    elif "Invalid sample rate" in str(e):
         print(f"💡 Tip: Your microphone might not support the sample rate {SAMPLE_RATE} Hz. Check available rates.")
    elif "PortAudioError" in str(e):
         print("💡 Tip: Ensure you have PortAudio installed (often needed by sounddevice). Check sounddevice documentation.")
    exit(1)
