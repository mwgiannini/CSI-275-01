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

from ast import Raise
from distutils.log import ERROR
from multiprocessing import connection
import re
import socket

HOST = "localhost"
PORT = 20000
BACKLOG = 20
BUFFSIZE = 4096
ENCODING = 'ascii'
ERROR_MESSAGE = "ERROR".encode(ENCODING)

class SortServer:
    """A server for sorting numbers"""

    def __init__(self, host, port):
        """Create and bind to a listening TCP socket"""

        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.bind((host, port))
        pass

    def read_sort_parameter(self, request):
        """Reads a sorting parameter off the end of the request
        
        Returns the parameter as a character
        Throws an exception if the sort parameter is invalid
        """
        request_length = len(request)
        request_split = request.split('|')

        if len(request_split[0]) == request_length:
            return request_split[0], 'a'
        elif request_split[1] not in "ads":
            raise Exception("Invalid sort parameter!")
        else:
            return request_split[0], request_split[1]

    def run_server(self):
        """Open the SortServer to connections"""

        # Listen for a connection
        self.listen_socket.listen(BACKLOG)

        # Accept a connection
        conn, address = self.listen_socket.accept()

        while True:
            # Get some data
            data = conn.recv(BUFFSIZE)
            request = data.decode(ENCODING)

            try:
                # Check for a sort parameter
                request, sort_parameter = self.read_sort_parameter(request)

                # Split the request into a list
                data_list = request.split(" ")

                # Check for errors in the list
                if(data_list.pop(0) != "LIST"):
                    raise Exception("LIST tag is absent!")

                if len(data_list) == 0:
                    raise Exception("List is empty!")

                for i, element in enumerate(data_list):
                    try:
                        data_list[i] = int(element)
                    except:
                        try:
                            data_list[i] = float(element)
                        except:
                            raise Exception("Element not numeric!")
            except:
                conn.sendall(ERROR_MESSAGE)
                continue

            # Sort data
            if(sort_parameter == 'a'):
                data_list.sort()
            if(sort_parameter == 'd'):
                data_list.sort(reverse=True)
            if(sort_parameter == 's'):
                data_list = [str(i) for i in data_list]
                data_list.sort()

            # Send response
            return_data = "SORTED"
            for element in data_list:
                return_data += " " + str(element)
            conn.sendall(return_data.encode(ENCODING))

if __name__ == "__main__":
    server = SortServer(HOST, PORT)
    server.run_server()