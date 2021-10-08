from distances import distance_graph
from package_hashtable import packages_hash

from collections import defaultdict
from datetime import datetime


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
        # where the hell do I put a trucks speed??

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

    # need a way to build delivery list consisting of packages and most efficient routes
    def build_delivery_list(self, packages_to_deliver, best_route):
        self.packages = packages_to_deliver
        self.truck_route = best_route
        # build dict with truck details, route, and packages


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

    for package in packages_hash.map:
        deliveries[package[1][1]].append(package[1])

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


def get_best_route(original_route):
    # for edge in distance_graph.edges.items():
    #     print(edge)

    # loop thru orig route
    # use dijk algorithm to find shortest route
    # save route to new list, then set truck_route to new list
    optimized_route = [{original_route[0]: 0}]
    index = 0

    print(len(original_route))

    for address in original_route:
        if original_route.index(address) < len(original_route):
            optimized_route.append(distance_graph.dijkstra(address, original_route[original_route.index(address) + 1]))
            print(optimized_route, sep=", ")
        else:
            optimized_route.append(distance_graph.dijkstra(address, original_route[0]))

    # optimized_route.append(distance_graph.dijkstra(original_route[0], None))

    for trip in optimized_route:
        print(trip)


truck1 = Truck()
truck2 = Truck()
truck3 = Truck()

# sort packages and allocate to trucks, need distance file for addresses
allocate_packages()
# determine routes for trucks based on algorithm
# get_best_route()
truck1.truck_route = get_best_route(truck1.truck_route)

# truck1.build_delivery_list()
