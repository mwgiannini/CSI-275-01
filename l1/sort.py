#     Author: MW Giannini
#     Class: CSI-275-01
#     Assignment: Lab 1
#     Date Assigned: Jan 18th 2022
#     Due Date: Jan 24th 2022
#     Description: A program to get a list of numbers from a user and sort it.
#     I certify that this is entirely my own work, except where I have given
#     fully-documented references to the work of others. I understand the definition and
#     consequences of plagiarism and acknowledge that the assessor of this assignment
#     may, for the purpose of assessing this assignment:
#     - Reproduce this assignment and provide a copy to another member of academic staff;
#     and/or
#     - Communicate a copy of this assignment to a plagiarism checking service (which may
#     then retain a copy of this assignment on its database for the purpose of future
#     plagiarism checking)


def build_list():
    keyword = "exit"
    numbers = []

    while True:
        userInput = input("Enter a number: ")

        if userInput == keyword:
            break

        try:
            number = float(userInput)
        except ValueError:
            print("That is not a valid input.")
        else:
            numbers.append(number)
    
    return numbers

def sort_list(unsortedList):
    unsortedList.sort()

def main():
    numberList = build_list()
    sort_list(numberList)
    print(numberList)

if __name__ == "__main__":
    main()