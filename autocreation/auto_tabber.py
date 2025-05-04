import time
from pynput import keyboard

# Create controller object
kb_controller = keyboard.Controller()

delay = 0.2 # Small delay between press and release

print("Starting to press Tab every 2 seconds (Press Ctrl+C to stop)...")
try:
    while True:
        print("Pressing Tab...")
        kb_controller.press(keyboard.Key.tab)
        time.sleep(delay)
        kb_controller.release(keyboard.Key.tab)
        time.sleep(3) # Wait for 2 seconds before the next press
except KeyboardInterrupt:
    print("\nTab automation stopped by user.")

print("Script finished.") 