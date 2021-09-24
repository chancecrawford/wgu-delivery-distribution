import logging
import sys
import time


# Main Menu options:
# search deliveries, enter new delivery
def user_interface():
    # user menu options
    options = input("Enter number for desired action. \n \n"
                    "[1] Create package to deliver \n"
                    "[2] Lookup delivery status \n \n"
                    "[0] Exit program \n"
                    )
    user_input_actions(options)


def user_input_actions(user_input):
    if user_input == "0":
        print("Thank you for using the WGUPS DLD scheduling system! \n \n"
              "Termination application...")
        time.sleep(2)
        sys.exit()
    if user_input == "1":
        print("case 1")
    if user_input == "2":
        print("case 2")


# How to do the delivery creation?
# step-by-step enter fields, insert into hashmap

# How to do the lookup?
# ask for numbered input tied to which field to search by, get user input, search deliveries with that input

print("Welcome to the WGUPS DLD scheduling system! \n")
user_interface()
