import sys
import time

from truck import truck1, truck2, truck3
from distances import distance_graph
from package_hashtable import packages_hash
from utils import verify_number_input


# ui for searching, creating package deliveries
def user_interface():
    # user options: search deliveries, enter new delivery
    options = input("Enter number for desired action. \n \n"
                    "[1] Create package to deliver \n"
                    "[2] Lookup delivery status \n"
                    "[3] See all packages \n"
                    "[4] Test \n \n"
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

        # verify id is an int
        if verify_number_input(package_id):
            new_package = [package_id, address, city, state, zip_code, deadline, weight, status]
            packages_hash.insert_package(new_package[0], new_package)
            print('Package #', package_id, ' inserted successfully!')

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
            if verify_number_input(search_id):
                search_results = [packages_hash.search_by_key(search_id)]

        # search by value in packages
        if search_choice == "2":
            search_value = input("Enter value to search for packages with. \n")
            search_results = packages_hash.search_by_value(search_value)

        # filter out None entries if id entered would try to grab something out of bounds of list
        filtered_search = [result for result in search_results if result is not None]
        # print results matching search if any
        if filtered_search:
            for result in filtered_search:
                print('---RESULT---', result)
        else:
            print("No packages found.")

    # show all packages/deliveries
    if options == "3":
        for entry in packages_hash.map:
            if entry is not None:
                print(entry)
    # show distance graph (only for testing/debugging)
    if options == "4":
        print('Truck1 Packages #: ', len(truck1.packages))
        print('Truck2 Packages #: ', len(truck2.packages))
        print('Truck3 Packages #: ', len(truck3.packages), "\n")

        print('TRUCK 1:', *truck1.packages, sep="\n")
        print('TRUCK 2:', *truck2.packages, sep="\n")
        print('TRUCK 3:', *truck3.packages, sep="\n")

        print('___Truck1 Route___', *truck1.truck_route, sep="\n")
        print('___Truck2 Route___', *truck2.truck_route, sep="\n")
        print('___Truck3 Route___', *truck3.truck_route, sep="\n")


print("Welcome to the WGUPS DLD scheduling system! \n")
user_interface()
