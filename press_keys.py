import time
from pynput import keyboard, mouse

# Create controller objects
kb_controller = keyboard.Controller()
mouse_controller = mouse.Controller()

delay = 0.05 # Small delay between actions

print("Sending Cmd + L...")
# Press Cmd + L
kb_controller.press(keyboard.Key.cmd)
time.sleep(delay)
kb_controller.press('l')
time.sleep(delay)
kb_controller.release('l')
time.sleep(delay)
kb_controller.release(keyboard.Key.cmd)

print("Waiting 0.5s...")
time.sleep(0.5)

print("Sending Ctrl + Cmd + T...")
# Press Ctrl + Cmd + T
kb_controller.press(keyboard.Key.ctrl)
time.sleep(delay)
kb_controller.press(keyboard.Key.cmd)  # Use Key.cmd for Command key on macOS
time.sleep(delay)
kb_controller.press('t')
time.sleep(delay)

# Release the keys in reverse order
kb_controller.release('t')
time.sleep(delay)
kb_controller.release(keyboard.Key.cmd)
time.sleep(delay)
kb_controller.release(keyboard.Key.ctrl)

print("Shortcuts sent!")


delay = 0.05 # Small delay between actions

print("Moving mouse to (950, 150)...")
mouse_controller.position = (950, 150)
time.sleep(delay * 2) # Give a bit more time for mouse movement

print("Clicking mouse...")
mouse_controller.click(mouse.Button.left, 1)
time.sleep(delay * 2)

print("Typing 'hello world'...")
kb_controller.type('hello world')
time.sleep(delay * 2)

print("Pressing Enter...")
kb_controller.press(keyboard.Key.enter)
time.sleep(delay)
kb_controller.release(keyboard.Key.enter)

print("Actions complete!")
