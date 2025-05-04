import librosa
import numpy as np
import sounddevice as sd
from scipy.spatial.distance import cosine
import os

# === Step 1: Load the reference sound ===
print("🔍 Loading reference sound...")
reference_fp = None
REFERENCE_SOUND_PATH = "sample.mp3" # Hardcoded value

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

# === Step 2: Define match threshold ===
# You might need to adjust this threshold based on your microphone sensitivity and environment noise.
# Try values between 0.7 and 0.95. Lower values are more lenient, higher values are stricter.
MATCH_THRESHOLD = 0.85 # Hardcoded value
print(f"ℹ️ Using match threshold: {MATCH_THRESHOLD}")


# === Step 3: Audio stream parameters ===
SAMPLE_RATE = 22050
# How often the script checks the audio (in seconds). Shorter durations are more responsive but use more CPU.
CHUNK_DURATION = 1.0 # Hardcoded value
BLOCKSIZE = int(SAMPLE_RATE * CHUNK_DURATION)

# === Step 4: Callback function for live microphone listening ===
def on_audio(indata, frames, time, status):
    if status:
        print(f"⚠️ Audio stream status: {status}")
    global reference_fp
    # Use only the first channel (mono)
    y = indata[:, 0]
    # Calculate MFCC features for the incoming audio chunk
    mfcc = librosa.feature.mfcc(y=y, sr=SAMPLE_RATE, n_mfcc=13)
    current_fp = np.mean(mfcc, axis=1)

    # Compare the fingerprint of the current chunk with the reference fingerprint
    # Cosine similarity ranges from -1 to 1. We use (1 - distance) to get similarity (closer to 1 is more similar).
    similarity = 1 - cosine(current_fp, reference_fp)

    # Optional: Print similarity score for debugging/tuning
    # print(f"Similarity: {similarity:.2f}")

    if similarity > MATCH_THRESHOLD:
        # --- ACTION TO TAKE ON MATCH ---
        print("👋 Hello world! (match score:", round(similarity, 2), ")")
        # You can replace the print statement with any other action,
        # like calling a function, sending a web request, etc.
        # Example: my_custom_function()

# === Step 5: Start listening ===
try:
    print(f"🎧 Listening for target sound (chunk duration: {CHUNK_DURATION}s)... (Ctrl+C to stop)")
    with sd.InputStream(callback=on_audio,
                        channels=1,
                        samplerate=SAMPLE_RATE,
                        blocksize=BLOCKSIZE,
                        dtype='float32'): # Ensure data type is float32 for librosa
        # Keep the script running indefinitely while the stream is active
        while True:
            sd.sleep(1000) # Sleep for 1 second intervals to avoid busy-waiting

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
