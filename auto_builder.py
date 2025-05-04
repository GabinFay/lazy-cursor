import librosa
import numpy as np
import sounddevice as sd
from scipy.spatial.distance import cosine
import os
import time
import threading
from pynput import keyboard, mouse
import sys

# === Configuration & Constants ===
# --- Sound Detection (Adjustable via Environment Variables or Defaults) ---
REFERENCE_SOUND_PATH = os.getenv("REFERENCE_SOUND_PATH", "sample.mp3") # Path to your AI completion sound
MATCH_THRESHOLD = float(os.getenv("MATCH_THRESHOLD", 0.9)) # How similar sound must be (0.8-0.98)
LOUDNESS_THRESHOLD_DB = float(os.getenv("LOUDNESS_THRESHOLD_DB", -35.0)) # How loud sound must be (-40 to -10)
CHUNK_DURATION = float(os.getenv("CHUNK_DURATION", 1.0)) # How often to check audio (seconds)
SAMPLE_RATE = 22050 # Sample rate for audio processing
BLOCKSIZE = int(SAMPLE_RATE * CHUNK_DURATION)

# --- Keyboard/Mouse Actions ---
ACTION_DELAY = 0.05 # Small delay between key presses/releases
POST_ACTION_DELAY = 0.5 # Delay after a sequence of actions (e.g., opening tab)
POST_TYPE_DELAY = 0.1 # Small delay after typing before Enter

# === Global Variables ===
kb_controller = keyboard.Controller()
mouse_controller = mouse.Controller() # Although unused in this specific workflow, keep if needed later
reference_fp = None # Fingerprint of the reference sound
sound_detected_event = threading.Event() # Used to signal sound detection

# === Sound Detection Functions ===
def load_reference(path):
    """Loads the reference sound file and computes its MFCC fingerprint."""
    if not os.path.exists(path):
        print(f"❌ Error: Reference sound file not found at '{path}'")
        print("Ensure the file exists or set the REFERENCE_SOUND_PATH environment variable.")
        sys.exit(1)
    try:
        print(f"⏳ Loading reference sound: {path}...")
        y, sr = librosa.load(path, sr=SAMPLE_RATE)
        if len(y) == 0:
            print(f"❌ Error: Reference sound file '{path}' is empty or could not be decoded.")
            sys.exit(1)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        fingerprint = np.mean(mfcc, axis=1)
        print("✅ Reference sound loaded successfully.")
        return fingerprint
    except Exception as e:
        print(f"❌ Error loading reference sound '{path}': {e}")
        sys.exit(1)

def on_audio_callback(indata, frames, time_info, status):
    """Callback function for the audio stream. Processes audio chunks."""
    if status:
        # Report issues but don't necessarily stop unless critical
        print(f"⚠️ Audio stream status: {status}", file=sys.stderr)
    global reference_fp, sound_detected_event
    if reference_fp is None:
        # Should not happen if load_reference is called first, but good practice
        print("❌ Error: Reference fingerprint not loaded.", file=sys.stderr)
        return

    try:
        # Use only the first channel (mono)
        y = indata[:, 0]

        # --- Calculate Loudness (dB) ---
        rms = np.sqrt(np.mean(y**2))
        decibels = 20 * np.log10(rms) if rms > 1e-9 else -np.inf # Avoid log(0)

        # --- Calculate MFCC Features ---
        mfcc = librosa.feature.mfcc(y=y, sr=SAMPLE_RATE, n_mfcc=13)
        current_fp = np.mean(mfcc, axis=1)

        # --- Compare Fingerprints ---
        # Ensure fingerprints are valid (e.g., not all NaNs)
        if np.isnan(current_fp).any() or np.isnan(reference_fp).any():
            # print("⚠️ Warning: NaN detected in fingerprint, skipping comparison.", file=sys.stderr)
            return

        similarity = 1 - cosine(current_fp, reference_fp)

        # Optional: Print scores for debugging/tuning
        # print(f"  Similarity: {similarity:.3f} (Threshold: {MATCH_THRESHOLD}), Loudness: {decibels:.1f} dB (Threshold: {LOUDNESS_THRESHOLD_DB})", end='')

        # --- Check both thresholds ---
        if similarity > MATCH_THRESHOLD and decibels > LOUDNESS_THRESHOLD_DB:
            print(f"🔊 Match Detected! (Similarity: {similarity:.3f}, Loudness: {decibels:.1f} dB)")
            if not sound_detected_event.is_set():
                sound_detected_event.set() # Signal the main loop

    except Exception as e:
        # Log errors during processing but allow the stream to continue if possible
        print(f"❌ Error in audio callback: {e}", file=sys.stderr)


def wait_for_completion_sound():
    """Listens for the target sound and blocks until detected."""
    global sound_detected_event
    sound_detected_event.clear() # Reset event for this listening phase
    print(f"🎧 Listening for AI completion sound (Chunk: {CHUNK_DURATION}s)... Press Ctrl+C to stop.")

    stream = None # Initialize stream variable
    try:
        stream = sd.InputStream(callback=on_audio_callback,
                                channels=1, # Mono input
                                samplerate=SAMPLE_RATE,
                                blocksize=BLOCKSIZE,
                                dtype='float32')
        with stream:
            # Wait indefinitely until the event is set by the callback
            while not sound_detected_event.is_set():
                 time.sleep(0.1) # Prevent busy-waiting, allow Ctrl+C check

    except sd.PortAudioError as pae:
         print(f"❌ PortAudioError: {pae}")
         print("💡 Ensure microphone is connected, selected, and drivers are installed.")
         print("💡 Check if another application is exclusively using the microphone.")
         print("💡 Try different audio settings (SAMPLE_RATE, CHUNK_DURATION).")
         sys.exit(1)
    except ValueError as ve:
         print(f"❌ ValueError during audio streaming setup: {ve}")
         if "Invalid number of channels" in str(ve):
            print("💡 This script requires a mono (1-channel) input from the microphone.")
         elif "Invalid sample rate" in str(ve):
             print(f"💡 Microphone might not support the sample rate {SAMPLE_RATE} Hz.")
         sys.exit(1)
    except Exception as e:
        print(f"❌ An unexpected error occurred during listening: {e}")
        # Attempt to close stream if it was opened
        if stream is not None and not stream.closed:
             stream.close()
        sys.exit(1)
    # No finally block needed for stream closure due to 'with' statement

# === Keyboard/Mouse Action Functions ===
def press_release(key_or_char):
    """Presses and releases a single key or character."""
    kb_controller.press(key_or_char)
    time.sleep(ACTION_DELAY)
    kb_controller.release(key_or_char)
    time.sleep(ACTION_DELAY)

def press_combo(*keys):
    """Presses and holds multiple keys, then releases them in reverse order."""
    for key in keys:
        kb_controller.press(key)
        time.sleep(ACTION_DELAY)
    # Release in reverse order
    for key in reversed(keys):
        kb_controller.release(key)
        time.sleep(ACTION_DELAY)

def focus_chat_input():
    """Sends Cmd+L to focus the chat input in Cursor."""
    print("⚙️ Focusing chat input (Cmd+L)...")
    press_combo(keyboard.Key.cmd, 'l')
    time.sleep(POST_ACTION_DELAY)

def accept_changes():
    """Sends Cmd+Enter to accept changes in Cursor."""
    print("⚙️ Accepting changes (Cmd+Enter)...")
    press_combo(keyboard.Key.cmd, keyboard.Key.enter)
    time.sleep(POST_ACTION_DELAY) # Allow time for acceptance to register

def open_new_chat_tab():
    """Sends Ctrl+Cmd+T to open a new chat tab in Cursor."""
    print("⚙️ Opening new chat tab (Ctrl+Cmd+T)...")
    press_combo(keyboard.Key.ctrl, keyboard.Key.cmd, 't')
    # Increase delay slightly to ensure tab is fully ready for typing
    time.sleep(POST_ACTION_DELAY + 0.3)

def type_and_enter(text):
    """Types the given text and presses Enter."""
    print(f"⚙️ Typing: '{text[:60]}...'") # Log truncated text
    kb_controller.type(text)
    time.sleep(POST_TYPE_DELAY)
    print("⚙️ Pressing Enter...")
    press_release(keyboard.Key.enter)
    # Give AI/system time to register the Enter press and start processing
    time.sleep(POST_ACTION_DELAY)

# === Main Workflow ===
def main():
    global reference_fp
    print("🚀 Starting Auto Cursor Builder Script 🚀")
    print("-" * 40)

    # --- Load Reference Sound ---
    print("--- Sound Configuration ---")
    print(f"Reference Sound: '{REFERENCE_SOUND_PATH}'")
    print(f"Match Threshold: {MATCH_THRESHOLD}")
    print(f"Loudness Threshold (dB): {LOUDNESS_THRESHOLD_DB}")
    print(f"Audio Chunk Duration: {CHUNK_DURATION}s")
    reference_fp = load_reference(REFERENCE_SOUND_PATH)
    print("-" * 40)

    # --- Get Project Input ---
    try:
        project_description = input("📝 Enter the project you want to build: ")
        if not project_description.strip():
            print("❌ Project description cannot be empty. Exiting.")
            sys.exit(1)
    except EOFError:
        print("❌ No input received (EOF). Exiting.")
        sys.exit(1)
    print("-" * 40)

    # --- Perform Initial Setup ---
    print("🛠️ Performing Initial Setup Actions...")
    focus_chat_input() # Cmd+L might not be needed if Ctrl+Cmd+T focuses automatically
    open_new_chat_tab() # No need to accept before the very first tab

    initial_prompt = (
        f"build this app: {project_description}, please create a PRD.md for this app which will contain "
        f"the requirements for the app, and tell it also to create a list of tasks to achieve "
        f"the project in status.md. Tell it to be very concise in the PRD.md, keep it short. "
        f"But status.md should contain all our information about the project."
    )
    type_and_enter(initial_prompt)
    print("✅ Initial prompt sent to Cursor.")
    print("-" * 40)

    # --- Main Interaction Loop ---
    loop_count = 0
    try:
        while True:
            loop_count += 1
            print(f"--- Loop Cycle {loop_count} ---")

            # === Step 1: Wait for AI -> Proceed ===
            wait_for_completion_sound()
            print("▶️ Action: Proceed with build")
            accept_changes() # <-- Add accept before opening tab
            open_new_chat_tab()
            type_and_enter("let's proceed to build this app")

            # === Step 2: Wait for AI -> Summarize ===
            wait_for_completion_sound()
            print("▶️ Action: Summarize status")
            accept_changes() # <-- Add accept before opening tab
            open_new_chat_tab()
            type_and_enter("summarize our state of work in status.md")

            # === Step 3: Wait for AI -> Proceed (Start of next cycle's logic) ===
            # The loop automatically continues here, waiting for the next sound
            # before the next 'proceed' action at the start of the loop.

    except KeyboardInterrupt:
        print("🛑 User interrupted (Ctrl+C). Stopping script.")
    except Exception as e:
        print(f"❌ An unexpected error occurred in the main loop: {e}")
        # Consider logging traceback for debugging
        # import traceback
        # traceback.print_exc()
    finally:
        print("👋 Script finished.")
        # Ensure audio stream is closed if somehow left open (though 'with' should handle it)
        # sd.stop() # Might be needed depending on how sd handles exceptions/interrupts


if __name__ == "__main__":
    # Check for essential libraries early
    try:
        import librosa
        import numpy
        import sounddevice
        import scipy
        import pynput
    except ImportError as e:
        print(f"❌ Missing required library: {e.name}")
        print("💡 Please install the required libraries. You might need:")
        print("   pip install librosa sounddevice numpy scipy pynput")
        # Note: librosa might require ffmpeg to be installed on the system
        if e.name == 'librosa':
             print("   (librosa may also require ffmpeg: check its documentation)")
        sys.exit(1)

    main() 