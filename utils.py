import datetime
import time


# for varying validations and utility functions
# validates user input is an int for searching package IDs
def verify_package_id_input(user_input):
    if user_input.strip().isdigit() and int(user_input) < 100:
        return True
    else:
        print("Please enter a number for package ID. \n")


# validates user input is proper time format
def verify_time_input(user_time_input):
    try:
        time.strptime(user_time_input, "%H:%M")
    except ValueError:
        print("Please enter a valid time in the HH:MM AM/PM format.")
        return False
    return True


# takes time in military time format and converts to timedelta for easy comparison to start/end delivery times
def convert_time_input_to_datetime(time_input):
    (hours, minutes) = time_input.split(":")
    return datetime.timedelta(hours=int(hours), minutes=int(minutes))
