from distances import distance_graph
from package_hashmap import packages_hash
from utils import convert_time_input_to_datetime

from collections import defaultdict
from datetime import datetime, timedelta


# Class for truck object that handles delivery of packages using hash map
# Utilizes distances graph and algorithm to determine route
class Truck:

    def __init__(self):
        # need start, current, and end time for tracking deliveries
        self.route_start_time = None
        self.route_current_time = None
        self.route_finish_time = None
        # lists for tracking truck packages and route order
        self.packages = []
        self.truck_route = []
        # average truck speed
        self.avg_speed = 18

    def start_route(self, timestamp):
        self.route_start_time = timestamp

    def finish_route(self, timestamp):
        self.route_finish_time = timestamp

    # O(1)
    def add_package(self, package):
        # add package to delivery list
        self.packages.append(package)
        # add address to to route (could we just add vertex?)
        self.truck_route.append(package[1])

    # O(N)
    def remove_package(self, package):
        # remove specified package
        self.packages.remove(package)
        # remove address from route (could we also just have vertex here?)
        self.truck_route.remove(package[1])

    # clear all truck info for querying delivery info back to back
    # O(N) but can be improved to O(1) if utilizing libraries that better utilize garbage collection
    def clear_truck_info(self):
        self.packages.clear()
        self.truck_route.clear()
        self.route_start_time = None
        self.route_current_time = None
        self.route_finish_time = None


# allocate packages based on priority and special instructions
# O(N^2)
def allocate_packages():
    # add home hub to beginning of all truck routes
    truck1.truck_route.append("4001 South 700 East")
    truck2.truck_route.append("4001 South 700 East")
    truck3.truck_route.append("4001 South 700 East")
    # need to separate all packages by address
    delivery_addresses = []
    # add packages to matching addresses in dict
    deliveries = defaultdict(list)
    # list for holding packages with EOD deadline and no special instructions
    regular_packages = []
    # add packages in temp deliveries dict
    for package in packages_hash.map:
        if package is not None:
            # set status to "AT HUB"
            package[1][8] = "AT HUB"
            deliveries[package[1][1]].append(package[1])
    # get addresses for temp address list
    for address in deliveries:
        delivery_addresses.append(address)

    # prioritize packages that have specific deadlines or instructions first
    for address in delivery_addresses:
        for package in deliveries[address]:
            if package is not None:
                if package[5] == "9:00":
                    truck1.add_package(package)
                elif package[5] == "9:05" or (package[5] != "EOD" and package[7] == "Delayed---9:05"):
                    truck2.add_package(package)
                elif package[5] == "EOD" and package[7] == "Delayed---9:05":
                    truck3.add_package(package)
                elif package[5] == "10:30" and "Must be delivered with" in package[7]:
                    truck1.add_package(package)
                elif package[0] == "19":
                    truck1.add_package(package)
                elif package[7] == "Wrong address listed":
                    truck1.add_package(package)
                elif package[7] == "Can only be on truck 2":
                    truck2.add_package(package)
                    # packages that have this deadline but no special instructions
                elif package[5] == "10:30" and package[7] == "":
                    truck1.add_package(package)
                else:
                    # add rest of packages to be allocated to trucks
                    regular_packages.append(package)

    # separate loop to then allocate remaining packages that have no specific deadline or instructions
    for package in regular_packages:
        # check to make sure truck capacity is not exceeded
        if len(truck1.packages) < 16:
            truck1.add_package(package)
        elif len(truck2.packages) < 16:
            truck2.add_package(package)
        elif len(truck3.packages) < 16:
            truck3.add_package(package)
        else:
            print("Package " + package[0] + " could not be allocated.")

    # insert return to hub for truck 2 to pick up delayed packages
    truck2.truck_route.insert(12, "4001 South 700 East")
    # put delayed packages delivery addresses at end of list
    truck2.truck_route.append(truck2.truck_route.pop(truck2.truck_route.index("3060 Lester St")))
    truck2.truck_route.append(truck2.truck_route.pop(truck2.truck_route.index("5383 South 900 East #104")))


# takes in delivery list of addresses and optimizes travel distance
# O(N)
def get_best_route(original_route):
    # create blank list for storing optimized paths in route
    optimized_route = []
    # index for tracking when to add home hub at end of route
    # start at one to account for home hub already being in list
    index = 1
    # loop through addresses in route and get shortest distance routes/miles between each stop
    for address in original_route:
        # index check if stop is last stop or not
        if index < len(original_route):
            optimized_route.append(
                distance_graph.get_shortest_path(address, original_route[original_route.index(address) + 1]))
            index += 1
        # if it is last stop, add home hub and shortest route to it
        elif index == len(original_route):
            optimized_route.append(distance_graph.get_shortest_path(address, original_route[0]))
    # return optimized route for given truck
    return optimized_route


# runs delivery simulation, saves times for truck/package delivery start/finish,
# and updates statuses throughout simulation
# O(N^2)
def start_deliveries():
    # need to set start time for truck 1/2 at 8am
    truck1.start_route(datetime.today().replace(hour=8, minute=0))
    truck2.start_route(datetime.today().replace(hour=8, minute=0))
    # set current time to start time for adding travel times for each stop
    truck1.route_current_time = truck1.route_start_time
    truck2.route_current_time = truck2.route_start_time
    # update package statuses/start times for truck 1/2
    for package in truck1.packages:
        package[8] = "OUT FOR DELIVERY"
        package[9] = str(truck1.route_start_time)
    for package in truck2.packages:
        # pass over delayed packages when updating truck2 statuses
        if package[7] != "Delayed---9:05":
            package[8] = "OUT FOR DELIVERY"
            package[9] = str(truck2.route_start_time)
    # loop through truck routes and compute time taken to reach each hub
    # first truck route
    for truck1_delivery_stop in truck1.truck_route:
        # get decimal value of time to travel to stop
        time_to_deliver = float(truck1_delivery_stop[1]) / truck1.avg_speed
        # convert decimal to seconds to add to datetime
        time_to_deliver = round(time_to_deliver * 60 * 60, 2)
        # add time elapsed to current time
        truck1.route_current_time += timedelta(seconds=time_to_deliver)
        # update delivery statuses for packages delivered at this stop
        for package in truck1.packages:
            if truck1_delivery_stop[0] == package[1]:
                package[8] = "DELIVERED"
                package[10] = str(truck1.route_current_time)
    # update time that truck finishes route
    truck1.finish_route(truck1.route_current_time)

    # second truck route
    # need index for this trucks route to know when to load delayed packages
    route_index = 1  # start at 1 to skip over home hub at beginning of route
    for truck2_delivery_stop in truck2.truck_route:
        # get decimal value of time to travel to stop
        time_to_deliver = float(truck2_delivery_stop[1]) / truck2.avg_speed
        # convert decimal to seconds to add to datetime
        time_to_deliver = round(time_to_deliver * 60 * 60, 2)
        # add time elapsed to current time
        truck2.route_current_time += timedelta(seconds=time_to_deliver)
        # update delivery statuses for packages delivered at this stop
        route_index += 1
        for package in truck2.packages:
            if truck2_delivery_stop[0] == package[1]:
                package[8] = "DELIVERED"
                package[10] = str(truck2.route_current_time)
            # check if back at hub to pick up delayed packages
            if route_index == 12:
                if package[0] == "6" or package[0] == "25":
                    package[8] = "OUT FOR DELIVERY"
                    package[9] = str(truck2.route_current_time)

    # update time that truck finishes route
    truck2.finish_route(truck2.route_current_time)

    # have truck 3 route start when truck 1 finishes since all packages in truck 3 deadlines are EOD
    truck3.start_route(truck1.route_finish_time)
    truck3.route_current_time = truck3.route_start_time
    # update package statuses for truck 3
    for package in truck3.packages:
        package[8] = "OUT FOR DELIVERY"
        package[9] = str(truck3.route_start_time)
    # third truck route
    for truck3_delivery_stop in truck3.truck_route:
        # get decimal value of time to travel to stop
        time_to_deliver = float(truck3_delivery_stop[1]) / truck3.avg_speed
        # convert decimal to seconds to add to datetime
        time_to_deliver = round(time_to_deliver * 60 * 60, 2)
        # add time elapsed to current time
        truck3.route_current_time += timedelta(seconds=time_to_deliver)
        # update delivery statuses for packages delivered at this stop
        for package in truck3.packages:
            if truck3_delivery_stop[0] == package[1]:
                package[8] = "DELIVERED"
                package[10] = str(truck3.route_current_time)
    # update time that truck finishes route
    truck3.finish_route(truck3.route_current_time)


# iterates through all packages in temp list, compares desired time input to start/end times
# alters temp list to preserve original package info then returns temp list
# O(N^2)
def get_package_statuses(user_time_input):
    # parse input to convert to datetime
    converted_user_time_input_seconds = convert_time_input_to_datetime(user_time_input)
    # create temporary list for checking and altering packages to show statuses/start/end times at given time
    temp_package_list = packages_hash.map
    # loop through packages to determine status/start/end is at that time
    for package in temp_package_list:
        if package is not None:
            # convert start/end times in package to datetime then timedelta to compare to time input
            # first check if any times exist for start/end
            # if empty, place standard start times for packages
            if package[1][9] != "":
                start_datetime = datetime.strptime(package[1][9], "%Y-%m-%d %H:%M:%S.%f")
                start_time = timedelta(hours=start_datetime.hour, minutes=start_datetime.minute)
            else:
                # handle later delivery for truck 3
                if package[1] in truck3.packages:
                    start_time = truck1.route_finish_time
                else:
                    start_time = timedelta(hours=8, minutes=0)
            # if empty, place standard end times for packages
            if package[1][10] != "":
                end_datetime = datetime.strptime(package[1][10], "%Y-%m-%d %H:%M:%S.%f")
                end_time = timedelta(hours=end_datetime.hour, minutes=end_datetime.minute)
            else:
                end_time = timedelta(hours=17, minutes=0)

            # if time is before package has left hub
            if converted_user_time_input_seconds < start_time:
                package[1][8] = "AT HUB"
                package[1][9] = ""
                package[1][10] = ""
            # if package delivery has started but not been delivered
            if start_time <= converted_user_time_input_seconds < end_time:
                package[1][8] = "OUT FOR DELIVERY"
                package[1][10] = ""
            # if package has been delivered
            if converted_user_time_input_seconds >= end_time:
                package[1][8] = "DELIVERED"

    # return list with alterations to display current status/info and remove None entries
    return [row for row in temp_package_list if row is not None]


# get and compute miles traveled for each truck and total of all trucks
# O(N)
def get_truck_mileage():
    # create variables for storing mileage for each truck
    truck1_mileage = 0
    truck2_mileage = 0
    truck3_mileage = 0
    # loop through each route (after getting optimized routes and running delivery simulation) and compute mileage
    for delivery_stop in truck1.truck_route:
        truck1_mileage += delivery_stop[1]
    for delivery_stop in truck2.truck_route:
        truck2_mileage += delivery_stop[1]
    for delivery_stop in truck3.truck_route:
        truck3_mileage += delivery_stop[1]
    # display miles traveled for each truck
    print("Truck 1 Miles Traveled: ", str(round(truck1_mileage, 2)))
    print("Truck 2 Miles Traveled: ", str(round(truck2_mileage, 2)))
    print("Truck 3 Miles Traveled: ", str(round(truck3_mileage, 2)))
    # display total miles traveled by all trucks
    print("Total Miles Traveled By All Trucks: ", str(round(truck1_mileage + truck2_mileage + truck3_mileage, 2)))


# initialize each truck object
truck1 = Truck()
truck2 = Truck()
truck3 = Truck()
