""" A client for sending messages to a server using TLS.

Name: MW Giannini
Assignment: Lab 11
Class: CSI-275-01
Certificate of authenticitiy: I certify that this is entirely my own work,
except where code has been provided to me for the assignment.
"""
import socket, ssl

HOST = 'localhost'  # IP of server
PORT = 7778         # Port of server


def send_messages():
    """Collect text from the user and send it to our server."""
    # Create a variable for input
    user_input = ""

    # Create a context
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_cert_chain(certfile='cli_cert.crt', keyfile='cli_key.key')
    context.load_verify_locations('srv_cert.crt')

    # Create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    tls_sock = context.wrap_socket(sock, server_side=False, server_hostname=HOST)

    while user_input != "done":
        # Prompt the user for input
        user_input = input("Please enter a message, or 'done' to exit.")

        # Encode the message
        encoded_message = user_input.encode('ascii')

        # Send the message
        tls_sock.sendall(encoded_message)

    # Close the socket if the while loop exits
    tls_sock.close()


def main():
    """Call send_messages to start our message loop."""
    send_messages()


if __name__ == "__main__":
    main()

