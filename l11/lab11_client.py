"""Don't forget your docstrings!
"""
import socket

HOST = 'localhost'  # IP of server
PORT = 7778         # Port of server


def send_messages():
    """Collect text from the user and send it to our server."""
    # Create a variable for input
    user_input = ""

    # Create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    while user_input != "done":
        # Prompt the user for input
        user_input = input("Please enter a message, or 'done' to exit.")

        # Encode the message
        encoded_message = user_input.encode('ascii')

        # Send the message
        sock.sendall(encoded_message)

    # Close the socket if the while loop exits
    sock.close()


def main():
    """Call send_messages to start our message loop."""
    send_messages()


if __name__ == "__main__":
    main()

