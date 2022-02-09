"""A UDP client with exponential backoff and request IDs.

Author: MW Giannini
Class: CSI-275-01
Assignment: UDP Client

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
import constants
import random


class TimeOutError(Exception):
    """Exception raised when a socket times out."""

    pass


class UDPClient:
    """A client to send UDP messages."""

    server_info = None
    udp_socket = None
    request_id_enabled = None
    DEBUG = False

    def __init__(self, host, port, request_id_enabled=False):
        """Initialize a UDP Client.

        Save the server data and connect with a UDP socket
        """
        self.server_info = (host, port)
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.connect(self.server_info)
        self.request_id_enabled = request_id_enabled

    def __del__(self):
        """Destroy a UDP Client.

        Close the socket
        """
        self.udp_socket.close()

    def send_character(self, character):
        """Send one character to the server.

        Returns a request ID or None if ids are disabled
        """
        request_id = None

        # Prepare data
        if self.request_id_enabled:
            data_to_send, request_id = create_request(character)
        else:
            data_to_send = character.encode('ascii')

        # Send data
        self.udp_socket.sendto(data_to_send, self.server_info)
        if self.DEBUG:
            print("sent " + data_to_send.decode('ascii'))  # ---------------->
        return request_id

    def receive_char(self, request_id=None):
        """Receive one character from the server.

        Returns a single character, Will verify request IDs if enabled.
        """
        valid_response = False
        while not valid_response:
            # Try to receive the data
            data, address = self.udp_socket.recvfrom(constants.MAX_BYTES)
            decoded_char = data.decode('ascii')
            if self.DEBUG:
                print("received " + decoded_char)  # ------------------------>

            if not self.request_id_enabled:
                return decoded_char

            valid_response = check_request(decoded_char, request_id)
        return decoded_char.split('|')[1]

    def send_message_by_character(self, message):
        """Send a message one character at a time.

        Will verify request IDs if enabled
        """
        output = ""

        for character in message:
            seconds_to_wait = constants.INITIAL_TIMEOUT

            while seconds_to_wait < constants.MAX_TIMEOUT:
                request_id = self.send_character(character)
                self.udp_socket.settimeout(seconds_to_wait)

                try:
                    output += self.receive_char(request_id)
                    break
                except socket.timeout:
                    seconds_to_wait *= 2
            else:
                raise TimeOutError

        return output


def create_request(message):
    """Concatenate a request ID to a message.

    Returns a tuple containing the ascii encoded bytestring and request ID
    """
    output = ""
    request_id = random.randrange(0, constants.MAX_ID)
    output += str(request_id)
    output += "|"
    output += message

    return output.encode('ascii'), request_id


def check_request(message, request_id):
    """Verify a message with a request ID.

    Returns True if the id matches
    """
    given_id = int(message.split('|')[0])
    return given_id == request_id


def main():
    """Run some basic tests on the required functionality.

    for more extensive tests run the autograder!
    """
    client = UDPClient(constants.HOST, constants.ECHO_PORT)
    print(client.send_message_by_character("hello world"))

    client = UDPClient(constants.HOST, constants.REQUEST_ID_PORT, True)
    print(client.send_message_by_character("hello world"))


if __name__ == "__main__":
    main()
