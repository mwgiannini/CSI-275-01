"""A UDP client with exponential backoff and request IDs

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

class UDPClient:
    server_data = None
    udp_socket = None

    def __init__(self, host, port):
        """Initialize a UDP Client
        
        Save the server data and connect with a UDP socket
        """
        self.server_data = (host, port)
        self.udp_socket = socket(type = socket.SOCK_DGRAM)
        self.udp_socket.connect(self.server_data)

    def __del__(self):
        """Destroy a UDP Client
        
        Close the socket
        """
        self.udp_socket.close()

    def send_message_by_character(self, message):
        """Send a message one character at a time
        
        
        """

        for character in message:
            self.udp_socket.settimeout(constants.INITIAL_TIMEOUT)

            # Encode and send the character
            encoded_char = character.encode()
            self.udp_socket.sendto(encoded_char, self.server_data)

            # Wait for a response
            data, address = self.udp_socket.recvfrom(4096)
            decoded_response = data.decode()




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
