""" A multithreaded client for chat messaging.

Name: MW Giannini
Assignment: Final Project
Class: CSI-275-01
Certificate of authenticitiy: I certify that this is entirely my own work,
except where code has been provided to me for the assignment.
"""
import socket
import json
import threading
import zlib


class MessageClient:
    """Chat client for connecting to the server."""

    SERVER_ADDRESS = 'localhost'
    SEND_PORT = 10000
    RECV_PORT = 10001
    LENGTH_FIELD_BYTES = 4

    def __init__(self):
        """Initialize a message client."""
        self.get_user_name()
        self.create_sockets()

        # Send start messages to both sockets to tell server username
        self.send_message(self.send_sock, 'START', message=self.user_name)
        self.send_message(self.recv_sock, 'START', message=self.user_name)

    def create_sockets(self):
        """Create and connect to two TCP sockets."""
        # Create TCP sockets
        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket
        self.send_sock.connect((self.SERVER_ADDRESS, self.SEND_PORT))
        self.recv_sock.connect((self.SERVER_ADDRESS, self.RECV_PORT))

    def get_user_name(self):
        """Get a valid username from the user."""
        self.user_name = input("Enter a username: ")

        # Check if the user name has spaces
        if " " in self.user_name:
            print("Username cannot contain spaces")
            self.get_user_name()

        # Check if the user name is a valid length
        elif len(self.user_name) < 3 or len(self.user_name) > 20:
            print("Username must be between 3 and 20 characters")
            self.get_user_name()

    def send_message(self, sock, message_type, message, recipient=None):
        """Send a message to the server."""
        message = {'type': message_type, 'message': message,
                   'from': self.user_name, 'recipient': recipient}
        
        # Format message
        json_message = json.dumps(message)
        bytes_message = json_message.encode()
        compr_message = zlib.compress(bytes_message)
        length = len(compr_message).to_bytes(self.LENGTH_FIELD_BYTES, 'big')

        sock.sendall(length + compr_message)

    def recv_message(self, sock):
        """Receive a single message from the given socket."""
        # Get the length from the length field
        length = int.from_bytes(
            sock.recv(self.LENGTH_FIELD_BYTES), 'big')

        # Get the message
        data = b''
        while len(data) < length:
            more = sock.recv(length - len(data))
            if not more:
                raise EOFError('was expecting %d bytes but only received'
                               ' %d bytes before the socket closed'
                               % (length, len(data)))
            data += more

        # Convert the message to a dictionary object
        bytes_message = zlib.decompress(data)
        decoded_message = bytes_message.decode()
        message = json.loads(bytes_message)
        return message

    def sock_handler(self, sock_type):
        """Handle errors for socket threads."""
        try:
            if sock_type == 'RECV':
                self.recv_main()
            elif sock_type == 'SEND':
                self.send_main()
        except ConnectionResetError:
            print('Connection error')
        except:
            print("Client socket has closed")
        finally:
            self.send_sock.close()
            self.recv_sock.close()

    def recv_main(self):
        """Listen for messages from the server and display to the user."""
        while True:
            message = self.recv_message(self.recv_sock)

            # Handle different types of messages
            if message['type'] == 'BROADCAST':
                print(f"{message['from']}: {message['message']}")

            elif message['type'] == 'PRIVATE':
                print(f"{message['from']} (private): {message['message']}")

    def send_main(self):
        """Listen for messages from user and send to the server."""
        while True:
            # Check the first word of user input for commands
            message = None
            while not message or message.isspace():
                message = input()
            command = message.split()[0]

            # Exit
            if command == '!exit':
                print("Disconnecting from the server...")
                return
            # Private
            elif command[0] == '@':
                recipient = command[1:]

                split_message = message.split(' ', 1)
                if len(split_message) > 1:
                    message = split_message[1]
                else:
                    message = ''
                self.send_message(self.send_sock, 'PRIVATE',
                                  message, recipient)
            # Broadcast
            else:
                self.send_message(self.send_sock, 'BROADCAST', message)


def main():
    client = MessageClient()

    # Create send/recv threads
    send_thread = threading.Thread(target=client.sock_handler, args=('SEND',))
    recv_thread = threading.Thread(target=client.sock_handler, args=('RECV',))

    send_thread.start()
    recv_thread.start()


if __name__ == "__main__":
    main()
