import time
from pynput import keyboard

# Create controller object
kb_controller = keyboard.Controller()

delay = 0.2 # Small delay between press and release

print("Starting automation: Tab -> 1s delay -> Enter -> 1s delay (Press Ctrl+C to stop)...")
try:
    while True:
        print("Pressing Tab...")
        kb_controller.press(keyboard.Key.tab)
        time.sleep(delay)
        kb_controller.release(keyboard.Key.tab)
        time.sleep(1) # Wait for 1 second

        print("Pressing Enter...")
        kb_controller.press(keyboard.Key.enter)
        time.sleep(delay)
        kb_controller.release(keyboard.Key.enter)
        time.sleep(2) # Wait for 1 second before the next cycle
except KeyboardInterrupt:
    print("\nAutomation stopped by user.")

print("Script finished.") 