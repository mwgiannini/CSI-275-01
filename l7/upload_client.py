"""A client with basic data framing capabilities.

Author: MW Giannini
Class: CSI-275-01
Assignment:

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

import argparse
import socket
import os
import constants


class UploadError(Exception):
    """Error when uploading."""

    pass


class UploadClient:
    """A client to upload files to a server."""

    def __init__(self, hostname, port) -> None:
        """Initialize the client by creating a socket."""
        self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_sock.connect((hostname, port))

        # Create a buffer to use with the recv_until_delimiter function
        self.buffer = b''

    def close(self) -> None:
        """Close the client's socket."""
        self.tcp_sock.close()

    def list_files(self) -> list[(str, int)]:
        """Request a list of files that have been uploaded to the server."""
        # Send the request to the server
        request = b'LIST\n'
        self.tcp_sock.sendall(request)

        # Initialize return value
        file_list = []

        # Receive the list from the server
        while True:
            # Get an element
            bytes = self.recv_until_delimiter(b'\n')

            if not bytes:
                return file_list

            # Convert element to a tuple
            filename, length = tuple(bytes.decode('ascii').split(" "))
            element = filename, int(length)

            file_list.append(element)

    def recv_all(self, length) -> bytes:
        """Receive data of fixed length from the socket.

        This function is modified from listing 3-1 of the textbook.
        """
        data = b''
        while len(data) < length:
            more = self.tcp_sock.recv(length - len(data))
            if not more:
                raise EOFError('was expecting %d bytes but only received'
                               ' %d bytes before the socket closed'
                               % (length, len(data)))
            data += more
        return data

    def recv_until_delimiter(self, delimiter) -> bytes:
        """Receive data from socket until the delimiter is reached."""
        delimiter_found = False

        data = b''

        while not delimiter_found:
            if self.buffer:
                # Start working with what data is in the buffer
                more = self.buffer
                self.buffer = b''

            else:
                # Start working with the data from socket
                more = self.tcp_sock.recv(constants.MAX_BYTES)

                # Check for EOFError
                if not more:
                    raise EOFError('The delimiter, %d was never received'
                                   ' %d bytes were received before the '
                                   'socket closed'
                                   % (delimiter, len(data)))

            # Split the incoming data at the first occurence of the delimiter
            more_split = more.split(delimiter, 1)

            # Append the first element to the return data
            data += more_split[0]

            # If a delimiter is removed, lengths are different
            delimiter_found = (len(more_split[0]) != len(more))

        # Store the data after the delimiter in the buffer
        self.buffer = more_split[1]

        return data

    def upload_file(self, file_path):
        """Upload a file to the class's server.

        The function handles Q4 of the original assignment.
        """
        # Open the file
        file = open(file_path, "rb")

        # Read the whole thing into memory
        file_data = file.read()

        # Prep the first line to send
        header = "UPLOAD " + os.path.basename(file_path) + " " \
                 + str(len(file_data)) + "\n"
        print(f"Sending {header}")

        self.tcp_sock.sendall(header.encode("ascii"))

        # Send the file data
        self.tcp_sock.sendall(file_data)

        # Wait for a response
        return_msg = self.recv_until_delimiter(b"\n").decode("ascii")
        if return_msg == "ERROR":
            raise UploadError
        else:
            print("Upload successful")


def main():
    """Run some basic tests on the required functionality.

    for more extensive tests run the autograder!
    """
    parser = argparse.ArgumentParser(description="TCP File Uploader")
    parser.add_argument("host", help="interface the server listens at;"
                        " host the client sends to")
    parser.add_argument("-p", metavar="PORT", type=int,
                        default=constants.UPLOAD_PORT,
                        help=f"TCP port (default {constants.UPLOAD_PORT})")
    args = parser.parse_args()
    upload_client = UploadClient(args.host, args.p)
    upload_client.upload_file("upload_client.py")
    print(upload_client.list_files())
    upload_client.close()


if __name__ == "__main__":
    main()
