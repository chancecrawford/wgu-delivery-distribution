# for varying validations and utility functions

def verify_package_id_input(user_input):
    if user_input.strip().isdigit() and int(user_input) < 100:
        return True
    else:
        print("Please enter a number for package ID. \n")
