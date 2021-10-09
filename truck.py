from distances import distance_graph
from package_hashtable import packages_hash

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

    def get_current_time(self):
        self.route_current_time = datetime.now()

    def finish_route(self, timestamp):
        self.route_finish_time = timestamp

    def add_package(self, package):
        # add package to delivery list
        self.packages.append(package)
        # add address to to route (could we just add vertex?)
        self.truck_route.append(package[1])

    def remove_package(self, package):
        # remove specified package
        self.packages.remove(package)
        # remove address from route (could we also just have vertex here?)
        self.truck_route.remove(package[1])

    # I don't think we need this anymore??
    # need a way to build delivery list consisting of packages and most efficient routes
    # def build_delivery_list(self, packages_to_deliver, best_route):
    #     self.packages = packages_to_deliver
    #     self.truck_route = best_route


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
    # add packages in temp deliveries dict
    for package in packages_hash.map:
        if package is not None:
            deliveries[package[1][1]].append(package[1])
    # get addresses for temp address list
    for address in deliveries:
        delivery_addresses.append(address)

    # 3 trucks, 2 drivers, don't worry about gas, no time taken to deliver or switch trucks
    # one of trucks have to return base hub to switch trucks -- can't carry all in 2
    # have to figure out how to deal with packages not arriving to hub until 9:05
    # # manually insert home hub for truck to go back to
    # trucks avg speed = 18mph
    regular_packages = []

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
                elif package[7] == "Can only be on truck 2":
                    truck2.add_package(package)
                    # packages that have this deadline but no special instructions
                elif package[5] == "10:30" and package[7] == "":
                    truck1.add_package(package)
                    # add rest of packages not to exceed 16 on each truck
                else:
                    regular_packages.append(package)

    # separate loop to then allocate remaining packages that have no specific deadline or instructions
    for package in regular_packages:
        # if package[5] == "EOD" and package[7] == "":
        if len(truck1.packages) < 16:
            truck1.add_package(package)
        elif len(truck2.packages) < 16:
            truck2.add_package(package)
        elif len(truck3.packages) < 16:
            truck3.add_package(package)
        else:
            print("Package " + package[0] + " could not be allocated.")


# O(N)
# TODO: need to adjust for truck 2 returning to hub to pick up late arrival packages
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
            optimized_route.append(distance_graph.dijkstra(address, original_route[original_route.index(address) + 1]))
            index += 1
        # if it is last stop, add home hub and shortest route to it
        elif index == len(original_route):
            optimized_route.append(distance_graph.dijkstra(address, original_route[0]))
    # return optimized route for given truck
    return optimized_route


def start_deliveries():
    # need to set start time for truck 1/2 at 8am
    truck1.start_route(datetime.today().replace(hour=8, minute=0))
    truck2.start_route(datetime.today().replace(hour=8, minute=0))
    # set current time to start time for adding travel times for each stop
    truck1.route_current_time = truck1.route_start_time
    truck2.route_current_time = truck2.route_start_time
    # loop through truck routes and compute time taken to reach each hub
    # first truck route
    for truck1_delivery_stop in truck1.truck_route:
        # get decimal value of time to travel to stop
        time_to_deliver = float(truck1_delivery_stop[1]) / truck1.avg_speed
        # convert decimal to seconds to add to datetime
        time_to_deliver = round(time_to_deliver * 60 * 60, 2)
        print(truck1_delivery_stop[0] + ": " + str(time_to_deliver))
        # add time elapsed to current time
        truck1.route_current_time += timedelta(seconds=time_to_deliver)
        # update delivery statuses for packages delivered at this stop
        for package in truck1.packages:
            if truck1_delivery_stop[0] == package[1]:
                package[8] = "DELIVERED"
                print("Package changed: ", package)
    # update time that truck finishes route
    truck1.finish_route(truck1.route_current_time)
    print("Truck1 Finish Time: ", str(truck1.route_finish_time))
    # second truck route
    for truck2_delivery_stop in truck2.truck_route:
        # get decimal value of time to travel to stop
        time_to_deliver = float(truck2_delivery_stop[1]) / truck2.avg_speed
        # convert decimal to seconds to add to datetime
        time_to_deliver = round(time_to_deliver * 60 * 60, 2)
        print(truck2_delivery_stop[0] + ": " + str(time_to_deliver))
        # add time elapsed to current time
        truck2.route_current_time += timedelta(seconds=time_to_deliver)
        # update delivery statuses for packages delivered at this stop
        for package in truck2.packages:
            if truck2_delivery_stop[0] == package[1]:
                package[8] = "DELIVERED"
                print("Package changed: ", package)
    # update time that truck finishes route
    truck2.finish_route(truck2.route_current_time)
    print("Truck2 Finish Time: ", str(truck2.route_finish_time))


# initialize each truck object
truck1 = Truck()
truck2 = Truck()
truck3 = Truck()

# sort packages and allocate to trucks, need distance file for addresses
allocate_packages()
# determine routes for trucks based on algorithm
truck1.truck_route = get_best_route(truck1.truck_route)
truck2.truck_route = get_best_route(truck2.truck_route)
truck3.truck_route = get_best_route(truck3.truck_route)
