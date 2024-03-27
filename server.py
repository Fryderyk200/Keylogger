import socket
HOST = '100.84.214.6'
PORT = 9090
FILE_NAME = 'received.txt'

def handle_client_connection(conn):
    received_data = conn.recv(1024).decode('utf-8')
    print(f"Received from client: {received_data}")

    response_message = 'restart_listener'
    conn.sendall(response_message.encode('utf-8'))
    print("Sent restart command to client.")

    with open(FILE_NAME, 'wb') as f:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            f.write(data)

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

        with open(FILE_NAME, 'rb') as f:
            contents = f.read().decode('utf-8')
            print(contents)

