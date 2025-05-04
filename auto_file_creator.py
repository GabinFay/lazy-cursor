import time
from pynput import keyboard

# Create controller object
kb_controller = keyboard.Controller()

delay = 0.05 # Small delay between actions

# Get user input
build_description = input("What do you want to build? ")

print("Starting automation...")
time.sleep(1) # Give a moment before starting

# Press Ctrl + N (or Cmd + N on macOS)
# Determine the correct modifier key based on the platform if needed,
# assuming Ctrl for now. Use Key.cmd for macOS if required.
print("Pressing Ctrl + N...")
kb_controller.press(keyboard.Key.cmd)
time.sleep(delay)
kb_controller.press('n')
time.sleep(delay)
kb_controller.release('n')
time.sleep(delay)
kb_controller.release(keyboard.Key.cmd)

print("Waiting...")
time.sleep(0.5) # Wait for the new file dialog/window

print("Typing filename 'testfile.py'...")
kb_controller.type('testfile.py')
time.sleep(delay * 2)

print("Pressing Enter...")
kb_controller.press(keyboard.Key.enter)
time.sleep(delay)
kb_controller.release(keyboard.Key.enter)

print("Waiting...")
time.sleep(0.5) # Wait for file to potentially open/be ready

print("Typing description as comment...")
kb_controller.type(f'# please build this app below this comment: {build_description} \n\nimport')
time.sleep(delay * 2)

print("Pressing Enter...")
kb_controller.press(keyboard.Key.enter)
time.sleep(delay)
kb_controller.release(keyboard.Key.enter)
time.sleep(delay * 2)


print("Starting to press Tab every 2 seconds (Press Ctrl+C to stop)...")
try:
    while True:
        print("Pressing Tab...")
        kb_controller.press(keyboard.Key.tab)
        time.sleep(delay)
        kb_controller.release(keyboard.Key.tab)
        time.sleep(2)
except KeyboardInterrupt:
    print("\nAutomation stopped by user.")

print("Script finished.") 