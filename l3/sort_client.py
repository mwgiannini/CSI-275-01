"""This is a client to demonstrate basic socket usage. Numbers are sent to the
server to be sorted.

Author: MW Giannini
Class: CSI-275-01
Assignment: Lab 3

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


def build_list():
    """ Builds a list of number from user input

    Pre: None
    Post: Returns a list of numbers
    """

    keyword = "exit"
    numbers = []

    while True:
        # Get a user input and check for exit keyword
        userInput = input("Enter a number: ")
        if userInput == keyword:
            break

        # Try to cast the input to a float
        try:
            number = float(userInput)

        # Give error message if the input is not a number
        except ValueError:
            print("That is not a valid input.")

        # Otherwise add the number to the list
        else:
            numbers.append(number)

    return numbers


def list_to_string(input_list):
    """ Converts a list to a string

    Pre: Given a list of numbers
    Post: Returns a formatted string
    """

    # Start with the LIST tag
    output = "LIST"

    # Add the numbers to the end
    for item in input_list:
        output += " " + str(item)
    return output


def string_to_list(input_string):
    """ Converts a string to a list

    Pre: Given a formatted string
    Post: Returns a list of numbers
    """
    # Split the string and remove the keyword
    split_list = input_string.split()
    split_list.pop(0)

    # Return the list with each element casted to float
    return [float(number) for number in split_list]


def sort_list(unsorted_list):
    """ Sends a list to the server to be sorted

    Pre: Given a list of numbers
    Post: Returns a sorted list
    """

    # Create the unsorted byte string
    unsorted_string = list_to_string(unsorted_list)
    byte_unsorted_string = unsorted_string.encode('ascii')

    # Create a net socket
    net_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("216.93.152.176", 7778)
    net_socket.connect(server_address)

    # Send the byte string to be sorted
    net_socket.sendall(byte_unsorted_string)

    # Receive the sorted string in return
    byte_sorted_string = b''
    while True:
        more = net_socket.recv(4096)
        if not more:
            break
        byte_sorted_string += more

    # Convert byte string back to a list
    sorted_string = byte_sorted_string.decode('ascii')
    sorted_list = string_to_list(sorted_string)

    net_socket.close()

    return sorted_list


def main():
    # Build a list of numbers from user input
    number_list = build_list()

    # Sort and print the list with the remote server
    sorted_list = sort_list(number_list)
    print(sorted_list)


if __name__ == "__main__":
    main()
