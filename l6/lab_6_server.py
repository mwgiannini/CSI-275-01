"""A server to determine the length of incoming TCP messages.

Author: MW Giannini
Class: CSI-275-01
Assignment: Lab 06

Certification of Authenticity:
I certify that this is entirely my own work, except where I have given
fully-documented references to the work of others. I understand the definition
and consequences of plagiarism and acknowledge that the assessor of this
assignment may, for the purpose of assessing this assignment:
- Reproduce this assignment and provide a copy to another member of academic
- staff; and/or Communicate a copy of this assignment to a plagiarism checking
- service (which may then retain a copy of this assignment on its database for
- the purpose of future plagiarism checking)
"""

import socket
HOST = "localhost"
PORT = 45000
BACKLOG = 20
LENGTH_FIELD_SIZE = 4
ENCODING = "ascii"

class LengthServer:
    """Create a server that return the length of received strings."""

    def __init__(self, host, port):
        """Create the socket and bind to it.
        
        Pre: Specify a host and port
        """
        self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_sock.bind((HOST, PORT))

    def calc_length(self):
        """Determine the length of incoming an incoming message"""

        self.tcp_sock.listen(BACKLOG)
        byte_length = self.tcp_sock.recv(LENGTH_FIELD_SIZE)
        length = byte_length.from_bytes(LENGTH_FIELD_SIZE, 'big')

        try:
            recvall(self.tcp_sock, length).decode(ENCODING)

        except EOFError:
            self.tcp_sock.sendall(b"Length Error")

        else:
            self.tcp_sock.sendall(f"I received {length} bytes.")
        

"""Receive a set length message from the socket
Cite: Function from provided client code

Pre: Provide socket and length in bytes
Post: Return data as a byte string
"""
def recvall(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('was expecting %d bytes but only received'
                           ' %d bytes before the socket closed'
                           % (length, len(data)))
        data += more
    return data

if __name__ == "__main__":
    server = LengthServer(HOST, PORT)
    server.calc_length()