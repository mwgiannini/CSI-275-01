"""A server to answer questions like a magic 8 ball by using multiple threads.

Name: MW Giannini
Class: CSI-275-01
Assignment: Lab 10: The Magic 8-Ball
Due: Monday, April 11th
Authenticity: I affirm that this work is entirely my own.
"""

from email import message
from logging.config import listen
import threading, socket, random

# Global list of 8-Ball answers
ANSWER_LIST = ["It is certain.",
               "It is decidedly so.",
               "Without a doubt.",
               "Yes - definitely.",
               "You may rely on it.",
               "As I see it, yes.",
               "Most likely.",
               "Outlook good.",
               "Yes.",
               "Signs point to yes.",
               "Reply hazy, ask again.",
               "Ask again later.",
               "Better not tell you now.",
               "Cannot predict now.",
               "Concentrate and ask again.",
               "Don't count on it.",
               "My reply is no.",
               "My sources say no.",
               "Outlook not so good.",
               "Very doubtful."]

# Server host/port information
HOST = "localhost"
SERVER_PORT = 8000

# Maximum amount of data to read in one function call
MAX_BYTES = 1024


class EightBallServer:
    """Server to answer questions like a magic 8 ball."""

    def __init__(self, host, port):
        """Create the initial listening socket and start our threads."""
        self.srv_sock = self.create_server_socket(host, port)

        self.start_threads(self.srv_sock)

    def create_server_socket(self, host, port):
        """Set up the 8-Ball server socket.

        Should go through the create/bind/listen steps and return
        the created listening socket.
        """
        listener = socket.socket()
        listener.bind((HOST, SERVER_PORT))
        listener.listen(20)
        return listener

    def accept_8ball_connections(self, listener):
        """Answer questions with Magic 8-Ball responses.

        This function should:
            - accept a connection from the listener socket
              (within our usual infinite while loop)
            - Use recv_until_delimiter() to grab questions from the client
              until it closes the socket ('?' will be the delimiter)
            - Provide a random response drawn from our 8-Ball answer set
              (see answer_list above) for each question
            - Send all of the answers as a single string back to the client,
            - and close the socket.
        """
        while True:
            tcp_sock, junk_address = listener.accept()
            buffer = b''
            replies = ''

            while tcp_sock:
                question, buffer = self.recv_until_delimiter(tcp_sock, b'?', buffer)

                # Ignore question and generate random reply
                replies += ANSWER_LIST[random.randint(0, len(ANSWER_LIST)-1)]
                
            tcp_sock.sendall(replies.encode())
            tcp_sock.close()

    def recv_until_delimiter(self, sock, byte_delim, storage):
        """Receive data until it sees a specified delimiter.

        This function returns two parameters: A complete message,
        and any extra data we currently have after the message (i.e.,
        what you should store in a buffer!)

        The delimiter should be passed to this function as a byte string.
        """
        # Initialize an empty buffer
        data = b""

        # For ease of use later
        delim_char = byte_delim.decode("ascii")
        index = 0

        # See if the message is already there
        for c in storage.decode("ascii"):
            if c != delim_char:  # No delimiter found yet
                data += c.encode("ascii")
                index += 1
            else:  # Delimiter found!
                # Put everything after the delimiter back into storage
                temp = storage[index+1:]
                storage = temp
                # Return the data and the current storage buffer
                return data, storage

        # If we get here, no delimiter yet
        delim_found = False
        while not delim_found:
            try:
                # Query the socket for more data
                more = sock.recv(MAX_BYTES)
            except ConnectionResetError:
                return b"", b""
            if not more:  # No more data to parse
                return b"", b""
            test = more.decode("ascii")
            index = 0
            for c in test:
                if c != delim_char:  # No delimiter found yet
                    data += c.encode("ascii")
                    index += 1
                else:  # Delimiter found!
                    # Put everything after the delimiter into storage
                    temp = test[index + 1:]
                    storage = temp.encode("ascii")
                    # Return the data and the current storage buffer
                    return data, storage

    def accept_connections_forever(self, sock):
        """Converse with a client over `sock` until they are done talking."""
        try:
            self.accept_8ball_connections(sock)
        except EOFError:
            print('Client socket has closed')
        except ConnectionResetError as e:
            print('Connection reset')
        finally:
            sock.close()

    # TODO Write this function!
    def start_threads(self, listener, workers=4):
        """Kick off the threads needed to serve 8-ball requests.

        Each thread should call accept_connections_forever() as its
        starting function.
        """
        self.threads = []
        # Create a list of threads as a member
        for i in range(0, workers):
            thread = threading.Thread(target=self.accept_connections_forever,args=(listener,))
            thread.start()
            self.threads.append(thread)


if __name__ == "__main__":
    eight_ball = EightBallServer(HOST, SERVER_PORT)