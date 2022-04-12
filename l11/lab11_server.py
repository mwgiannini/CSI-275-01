"""Don't forget your docstrings!
"""

import socket, ssl
import _thread

HOST = 'localhost'  # IP of server
PORT = 7778         # Port of server


def handler(client_socket, addr):
    """Receive messages and print them to the console."""
    while True:
        # Receive the data
        data = client_socket.recv(4096)
        if not data:
            break

        # Decode the data
        message = data.decode('ascii')

        # Print the message
        print(message)

    # If we break out of the loop, close the socket
    client_socket.close()


if __name__ == "__main__":
    # Create our listening socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(20)

    while True:
        # For every connection we get, spin off a new thread to
        # handle the accept socket
        client_sock, addr = sock.accept()
        _thread.start_new_thread(handler, (client_sock, addr))