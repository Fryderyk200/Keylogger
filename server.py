import socket
import ssl
from cryptography.fernet import Fernet
#Server IP address and port
HOST = '0.0.0.0'
PORT = 9090
#File name where  the decrypted data will be stored
FILE_NAME = 'received.txt'

def load_key():
    # attempt to load encrypted key from file
        try:
            with open("current_key.key", "rb") as key_file:
                key = key_file.read()
                return key
        except FileNotFoundError:
            # exeption if file not found print error message
            print("Encryption key file not fount")
            return None

#decrypt message using fernet
def decrypt_message(encrypted_message):
    key = load_key()
    if key is None:
        print("No decryption key available")
        return None
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    return decrypted_message.decode()

def handle_client_connection(conn):
    # initial response to the client
    response_message = 'continue'
    conn.sendall(response_message.encode('utf-8'))
    print("Sent 'continue' command to client.")

    #recive decrypt data
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

# Creates an ssl connection for secure communications
def create_ssl_context():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')
    return context


def main():
    context = create_ssl_context()
    ##sockets
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        print('Server listening... ')
        s.listen(5)

        while True:
            # accepts connection from clients
            conn, addr = s.accept()
            print(f"Accepted new connection from: {addr}")
            # wraps the connection with SSL
            with context.wrap_socket(conn, server_side=True) as secure_conn:
                # log initial message from client
                connected = secure_conn.recv(1024)
                print(connected)
                # receive a new encryption key from client
                receive_key = secure_conn.recv(1024)
                with open("current_key.key", "wb") as key_file:
                    key_file.write(receive_key)
                print("Received and saved new encryption key.")

                # handle further client communications
                handle_client_connection(secure_conn)


main()
