"""A client to send JSON encoded number lists to the server to be sorted.

Author: MW Giannini
Class: CSI-275-01
Assignment: Lab 9

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
import json
import socket
import zlib

def build_list():
    """Collect input from the user and return it as a list.

    Only numeric input will be included; strings are rejected.
    """
    sort_option = input("Please enter a sorting option:\n\
    1) 'a'- ascending\n\
    2) 'd'- descending\n\
    3) 's'- alphabetically\n")
    #Create a list to store our numbers
    unsorted_list = [sort_option]

    # Create a variable for input
    user_input = ""
    
    while user_input != "done":
        # Prompt the user for input
        user_input = input("Please enter a number, or 'done' to stop.")

        # Validate our input, and add it to out list
        # if it's a number
        try:
            # Were we given an integer?
            unsorted_list.append(int(user_input))
        except ValueError:
            try:
                # Were we given a floating-point number?
                unsorted_list.append(float(user_input))
            except ValueError:
                # Non-numeric input - if it's not "done",
                # reject it and move on
                if (user_input != "done"):
                    print ("ERROR: Non-numeric input provided.")
                continue

    # Once we get here, we're done - return the list
    return unsorted_list

def sort_list(unsorted_list):
    """Send a list to the server as json and receive the sorted result."""
    server_info = ("localhost", 7778)
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.connect(server_info)
    
    bytes_list = json.dumps(unsorted_list).encode('ascii')
    print(f"The list is {len(bytes_list)} bytes before compression.")
    compressed_list = zlib.compress(bytes_list)
    print(f"The list is {len(compressed_list)} bytes after compression.")
    tcp_sock.sendall(compressed_list)


    bytes_recv = tcp_sock.recv(4096)
    output = json.loads(zlib.decompress(bytes_recv).decode('ascii'))
    
    tcp_sock.close()
    return output


def main():
    """Call the build_list and sort_list functions, and print the result."""
    number_list = build_list()
    print(sort_list(number_list))

if __name__ == "__main__":
    main()

