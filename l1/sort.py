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