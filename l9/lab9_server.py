"""Server code for Lab 9.

Author: Duane Dunston (original author)
Author: Jason Reeves (modified code for CSI-275)
Author: MW Giannini (modified code for assignment)
Class: CSI-275-01/02
Assignment: Lab/HW 9 - JSON Client/Server

"""

from socket import *
import _thread
import time, datetime
import json
import zlib

HOST = 'localhost'  # IP of server
PORT = 7778         # Port of server


def handler(client_socket, addr):
    """Handler function for socket connections.

    Data submitted must be in the form "[num1 num2 ... numN]",
    where num1 through numN must be integers or floating-point numbers.

    """
    while True:
        # Receive the data
        data = client_socket.recv(4096)
        if not data:
            break

        # Decode the data into a list
        data_list = json.loads(zlib.decompress(data).decode('utf-8'))

        # Get time of connection
        now = datetime.datetime.now().timestamp()
        now_readable = time.ctime(now)

        # Print data and time of reception
        print(f"{now_readable}: Got {data} from {addr}")

        # Validate data
        is_error = False
        sort_option = data_list.pop(0)
        if type(sort_option) != str or sort_option not in "ads":
            print("Invalid sort option")
            is_error = True

        for element in data_list:
            try:
                # This will allow numeric data through
                float(element)
            except ValueError:  # Data is non-numeric
                print("Value Error")
                is_error = True

        return_data = ""
        if not is_error:
            # Sort data
            if sort_option == 'a':
                data_list.sort()
            if sort_option == 'd':
                data_list.sort(reverse=True)
            if sort_option == 's':
                data_list.sort(key=str)


            # Return the data to the client
            return_data = json.dumps(data_list)
        else:  # Error
            return_data = json.dumps(["ERROR"])

        # Send our response, whatever it may be
        print(f"Returning {return_data} to the client")
        client_socket.sendall(zlib.compress(return_data.encode('utf-8')))


if __name__ == "__main__":
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(20)

    while 1:
        client_sock, addr = sock.accept()
        _thread.start_new_thread(handler, (client_sock, addr))