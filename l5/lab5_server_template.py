"""A server to sort numbers.

Author: MW Giannini
Class: CSI-275-01
Assignment: Lab 05

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

from multiprocessing import connection
import socket

HOST = "localhost"
PORT = 20000
BACKLOG = 20
BUFFSIZE = 4096
ENCODING = 'ascii'

class SortServer:
    """A server for sorting numbers"""

    def __init__(self, host, port):
        "Create and bind to a listening TCP socket" 

        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.bind(host, port)
        pass

    def run_server(self):
        """Open the SortServer to connections"""

        # Listen for a connection
        self.listen_socket.listen(BACKLOG)

        # Accept a connection
        conn, address = self.listen_socket.accept()

        while True:
            data = conn.receive(BUFFSIZE)
            request = data.decode(ENCODING)


if __name__ == "__main__":
    server = SortServer(HOST, PORT)
    server.run_server()