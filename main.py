# Chance Crawford --- Student ID:

import sys
import time

import truck
from truck import truck1, truck2, truck3
from package_hashmap import packages_hash
from utils import verify_package_id_input, verify_time_input


# ui for searching, creating package deliveries, displaying delivery info
def user_interface():
    # bring up issue with wrong address at time that WGUPS finds out
    if not check_incorrect_package_updated():
        print("It is 10:20AM and Package #9 needs its address fixed... \n \n")
        time.sleep(1)
        correct_incorrect_address_input = input("Would you like to update it with the correct address? \n \n"
                                                "[0] Decline and return to main menu \n"
                                                "[1] Update address \n \n")
        # return to main menu if user declines
        if correct_incorrect_address_input == "0":
            print("Thank you for using the WGUPS DLD scheduling system! \n \n"
                  "Terminating application...")
            time.sleep(2)
            sys.exit()
        elif correct_incorrect_address_input == "1":
            # update package address
            for package in packages_hash.map:
                if package is not None:
                    if package[1][0] == "9":
                        package[1][1] = "410 S State St"
                        package[1][2] = "Salt Lake City"
                        package[1][3] = "UT"
                        package[1][4] = "84111"
                        package[1][7] = ""
                        print("Package #9 address updated! \n")
                        time.sleep(1)
        # return to main menu for check to make sure package #9 updated
        user_interface()

    # user options
    options = input("\nEnter number for desired action. \n \n"
                    "[1] Create package to deliver \n"
                    "[2] Lookup package \n"
                    "[3] See all packages \n"
                    "[4] See package status at specific time \n"
                    "[5] Show Truck Travel Mileage \n \n"
                    "[0] Exit program \n"
                    )

    # determine actions from selection
    # exit program
    if options == "0":
        print("Thank you for using the WGUPS DLD scheduling system! \n \n"
              "Terminating application...")
        time.sleep(2)
        sys.exit()
    # create package delivery
    if options == "1":
        # get all inputs needed for inserting new package into hashmap/csv
        package_id = input("Please enter the package id. (must be unique and less than 100) \n")
        address = input("Please enter the destination address \n")
        city = input("Please enter the destination city. \n")
        state = input("Please enter the destination state. \n")
        zip_code = input("Please enter the destination zip code. \n")
        deadline = input("Please enter the deadline the package must be delivered by. \n")
        weight = input("Please enter the package weight. (in kilos) \n")
        notes = input("Please enter any special instructions for the package. \n")
        status = input("Please enter the delivery status. (AT HUB, DELIVERED, OUT FOR DELIVERY) \n")
        start, end = "", ""

        # verify id is an int
        if verify_package_id_input(package_id):
            new_package = [package_id,
                           address,
                           city,
                           state,
                           zip_code,
                           deadline,
                           weight,
                           notes,
                           status,
                           start,
                           end]
            packages_hash.insert_package(new_package[0], new_package)
            print('Package #', package_id, ' inserted successfully!')
        # return to main menu
        user_interface()

    # search deliveries
    if options == "2":
        search_results = []
        search_choice = input("Search by package id or by delivery attribute? \n \n"
                              "[1] Package ID \n"
                              "[2] Delivery attribute \n")

        # search by package id
        if search_choice == "1":
            search_id = input("Enter package id... \n")
            # verify id is an int
            if verify_package_id_input(search_id):
                search_results = [packages_hash.search_by_key(search_id)]

        # search by value in packages
        if search_choice == "2":
            search_value = input("Enter value to search for packages with. \n")
            search_results = packages_hash.search_by_value(search_value)

        # print results matching search if any
        if search_results is not None:
            print('---Packages Matching Search Criteria--- \n')
            for result in search_results:
                print(", ".join(result))
        else:
            print("No packages found.")

        # return to main menu
        user_interface()

    # show all packages/deliveries
    # will change to display all package info at latest time search from option 4
    # O(N)
    if options == "3":
        # run functions to allocate packages to all 3 trucks and build delivery list
        truck.allocate_packages()
        # run addresses from delivery list through optimization algorithm (dijkstra's)
        truck.get_best_route()
        # run delivery simulation
        truck.start_deliveries()

        print("--- All Packages --- \n")
        for entry in packages_hash.map:
            if entry is not None:
                print(", ".join(entry[1]))

        # clear all delivery info for rerunning future queries
        truck1.clear_truck_info()
        truck2.clear_truck_info()
        truck3.clear_truck_info()
        # return to main menu
        user_interface()

    # show status of all packages at requested time
    # O(N) -- not including functions called from other files
    if options == "4":
        # get user desired time for package/delivery info
        user_time_input = input(
            "Please enter the time you wish to see package statuses for in military time. (Ex: 14:00) \n")
        # verify input is valid time format
        if verify_time_input(user_time_input):
            # run functions to allocate packages to all 3 trucks and build delivery list
            truck.allocate_packages()
            # run addresses from delivery list through optimization algorithm (dijkstra's)
            truck.get_best_route()
            # run delivery simulation
            truck.start_deliveries()
            # get package info at given time
            package_info_list = truck.get_package_statuses(user_time_input)
            # headers for easier data readability
            print("--- Package statuses at ", user_time_input, " --- \n"
                                                               "Package # \t Destination \t \t Status")
            # show needed package info for every package
            for row in package_info_list:
                print("\t" + row[1][0] + "\t \t" + row[1][1] + "\t \t" + row[1][8])

            # clear all delivery info for rerunning future queries
            truck1.clear_truck_info()
            truck2.clear_truck_info()
            truck3.clear_truck_info()
            # return to main menu
            user_interface()

    if options == "5":
        # run functions to allocate packages to all 3 trucks and build delivery list
        truck.allocate_packages()
        # get optimized routes for truck deliveries
        truck.get_best_route()
        # run delivery simulation
        truck.start_deliveries()
        # get and display truck mileage
        truck.get_truck_mileage()
        # clear all delivery info for rerunning future queries
        truck1.clear_truck_info()
        truck2.clear_truck_info()
        truck3.clear_truck_info()
        # return to main menu
        user_interface()


# used to check if package with incorrect address has been updated
# O(1) -- since searching with hash key
def check_incorrect_package_updated():
    package_nine = packages_hash.search_by_key("9")
    if package_nine[1] == "410 S State St":
        return True
    else:
        return False


print("Welcome to the WGUPS DLD scheduling system! \n")
user_interface()
