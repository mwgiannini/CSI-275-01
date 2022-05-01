""" A multithreaded server for chat messaging.

Name: MW Giannini
Assignment: Final Project
Class: CSI-275-01
Certificate of authenticitiy: I certify that this is entirely my own work,
except where code has been provided to me for the assignment.
"""
import socket
import threading
import json
import zlib

class MessageServer:
    """Chat server for multiple clients."""

    SERVER_ADDRESS = 'localhost'
    READ_PORT = 10000
    WRIT_PORT = 10001
    LENGTH_FIELD_BYTES = 4

    def __init__(self):
        """Initialize a message server."""
        print("Starting server...")
        self.connected_clients = {}
        self.create_sockets()

    def create_sockets(self):
        """Create and connect to two TCP sockets."""
        # Create TCP sockets
        self.read_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.writ_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket
        self.read_listener.bind((self.SERVER_ADDRESS, self.READ_PORT))
        self.writ_listener.bind((self.SERVER_ADDRESS, self.WRIT_PORT))

        self.read_listener.listen()
        self.writ_listener.listen()

    def recv_message(self, sock):
        """Receive a single message from the given socket.
        
        Returns message and metadata as a dictionary
        """

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
        try:
            bytes_message = zlib.decompress(data)
            decoded_message = bytes_message.decode()
            message = json.loads(bytes_message)
        
        except:
            # Handles users disconnecting prematurely
            message = None
        return message

    def reading_connection(self, sock, user):
        """Process commands from a connected client."""
        while True:
            message = self.recv_message(sock)

            if not message or message['type'] == 'EXIT':
                # Close the users sockets and remove from connections dictionary
                self.connected_clients[user].close()
                del self.connected_clients[user]
                sock.close()
                print(f"{user} has disconnected")
                return

            elif message['type'] == 'BROADCAST':
                # Send to all connected users
                for client in self.connected_clients:
                    if client != user:
                        self.send_message(self.connected_clients[client], message)
            
            elif message['type'] == 'PRIVATE':
                # Send to the recipient
                try:
                    recipient = message['recipient']
                    self.send_message(self.connected_clients[recipient], message)
                except KeyError:
                    message = {'type': 'PRIVATE', 'message': "Error: user does not exist!",
                    'from': 'SERVER'}
                    self.send_message(self.connected_clients[user], message)
            

    def reading_main(self):
        """Accept reading connections from a client."""
        while True:
            # Accept a connection
            sock, server_address = self.read_listener.accept()

            # Receive a START message to get the users name
            message = self.recv_message(sock)
            user = message['from']

            # Start a new thread to handle the connection with this client
            new_thread = threading.Thread(target=self.reading_connection, args=(sock, user))
            new_thread.start()

    def send_message(self, sock, message):
        """Send a message to a client."""
        # Format message
        json_message = json.dumps(message)
        bytes_message = json_message.encode()
        compr_message = zlib.compress(bytes_message)
        length = len(compr_message).to_bytes(self.LENGTH_FIELD_BYTES,'big')

        sock.sendall(length + compr_message)

    def sock_handler(self, sock_type):
        """Handle errors for socket threads."""
        try:
            if sock_type == 'READ':
                self.reading_main()
            elif sock_type == 'WRIT':
                self.writing_main()
        except EOFError:
            print('Client socket has closed')
        except ConnectionResetError:
            print('Connection error')

    def writing_main(self):
        """Accept writing connections from a client."""
        while True:
            # Accept a connection
            sock, server_address = self.writ_listener.accept()

            # Receive the START message and add the socket to the connections
            message = self.recv_message(sock)
            message_from = message['from']
            self.connected_clients[message_from] = sock

            print(f"User {message['from']} connected")


def main():
    server = MessageServer()
    
    # Create read/write threads
    read_thread = threading.Thread(target=server.sock_handler, args=('READ',))
    writ_thread = threading.Thread(target=server.sock_handler, args=('WRIT',))

    read_thread.start()
    writ_thread.start()

if __name__ == "__main__":
    main()