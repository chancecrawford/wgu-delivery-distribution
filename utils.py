# for varying validations and utility functions

def verify_number_input(user_input):
    print('hit validation')
    if user_input.strip().isdigit():
        return True
    else:
        print("Please enter a number for package ID.")

