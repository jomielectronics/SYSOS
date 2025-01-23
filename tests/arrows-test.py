# import pyautogui as typer

# typer.typewrite('pyautogui')
# import json

# with open("user.sysos", "r+") as f:
#     temp = json.load(f)
#     usrN = temp["Username"]

# print(usrN)


from pynput import keyboard
import threading
import time

# Function to handle key press events
def on_press(key):
    try:
        if key == keyboard.Key.up:  # Check if the pressed key is the Up Arrow key
            print('You Pressed the Up Arrow Key!')  # Print a message
            return False  # Stop the listener
    except AttributeError:
        pass  # Handle special keys that don't have a char attribute

# Function to run concurrently
def run_concurrently():
    while True:
        print("Running other code...")  # This simulates other work being done
        time.sleep(1)  # Sleep for a second to avoid flooding the output

# Create and start the keyboard listener in a separate thread
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Run the other code in the main thread
run_concurrently()

# Wait for the listener to stop before exiting
listener.join()
