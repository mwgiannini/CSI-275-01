""" A server for receiving messages from a client using TLS.

Name: MW Giannini
Assignment: Lab 11
Class: CSI-275-01
Certificate of authenticitiy: I certify that this is entirely my own work,
except where code has been provided to me for the assignment.
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
    # Create context
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile='srv_cert.crt', keyfile='srv_key.key')
    context.load_verify_locations('cli_cert.crt')

    # Create our listening socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(20)

    while True:
        # For every connection we get, spin off a new thread to
        # handle the accept socket
        client_sock, addr = sock.accept()
        tls_sock = context.wrap_socket(client_sock, server_side=True)
        _thread.start_new_thread(handler, (tls_sock, addr))