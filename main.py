import sys
import time

from package_hashtable import packages


# ui for searching, creating package deliveries
def user_interface():
    # user options: search deliveries, enter new delivery
    options = input("Enter number for desired action. \n \n"
                    "[1] Create package to deliver \n"
                    "[2] Lookup delivery status \n"
                    "[3] See all packages \n \n"
                    "[0] Exit program \n"
                    )

    # determine actions from selection
    # exit program
    if options == "0":
        print("Thank you for using the WGUPS DLD scheduling system! \n \n"
              "Termination application...")
        time.sleep(2)
        sys.exit()
    # create package delivery
    if options == "1":
        # get all inputs needed for inserting new package into hashtable/csv
        package_id = input("Please enter the package id. (must be unique) \n")
        address = input("Please enter the destination address \n")
        city = input("Please enter the destination city. \n")
        state = input("Please enter the destination state. \n")
        zip_code = input("Please enter the destination zip code. \n")
        deadline = input("Please enter the deadline the package must be delivered by. \n")
        weight = input("Please enter the package weight. (in kilos) \n")
        status = input("Please enter the delivery status. (at hub, delivered, en route \n")

        new_package = [package_id, address, city, state, zip_code, deadline, weight, status]
        packages.insert_package(new_package[0], new_package)

        print('Package #', package_id, ' inserted successfully!')

    # search deliveries
    if options == "2":
        search_results = []
        search_choice = input("Search by package id or by delivery attribute? \n \n"
                              "[1] Package ID \n"
                              "[2] Delivery attribute \n")
        # have user choose how to search for a package/delivery
        if search_choice == "1":
            # TODO: make sure only numbers can be input
            search_id = input("Enter package id... \n")
            search_results = packages.search_by_key(search_id)
        if search_choice == "2":
            search_value = input("Enter value to search for packages with. \n")
            search_results = packages.search_by_value(search_value)

        # print results matching search if any
        if search_results is not None:
            print(len(search_results), ' packages found. \n')
            for result in search_results:
                # prints key and values separately ?
                print(result)
        else:
            print("No packages found.")

    if options == "3":
        for entry in packages.map:
            if entry is not None:
                print(entry)


# How to do the delivery creation?
# step-by-step enter fields, insert into hashmap

# How to do the lookup?
# ask for numbered input tied to which field to search by, get user input, search deliveries with that input

print("Welcome to the WGUPS DLD scheduling system! \n")
user_interface()
