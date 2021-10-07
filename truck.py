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
    # need to separate all packages by address
    # packages_by_address = {addresses[i][2]: [] for i in range(0, len(addresses))}
    # add packages to matching addresses in dict
    # distance_graph.get_packages_for_delivery(packages_hash.map)

    delivery_addresses = []
    deliveries = defaultdict(list)

    # for package in packages_hash.map:
    #     print('Addr: ', package[1][1])

    for package in packages_hash.map:
        deliveries[package[1][1]].append(package[1])

    for address in deliveries:
        delivery_addresses.append(address)

    print('deliveries ', deliveries)
    for entry in deliveries.items():
        print(entry)

    for address in delivery_addresses:
        for package in deliveries[address]:
            if package is not None:
                if package[5] == "9:00":
                    truck1.add_package(package)
                if package[5] == "9:05" or package[7] == "Delayed---9:05":
                    truck2.add_package(package)
                if package[5] == "10:30" and "Must be delivered with" in package[7]:
                    truck1.add_package(package)
                if package[7] == "Can only be on truck 2":
                    truck2.add_package(package)
                    # packages that have this deadline but no special instructions
                if package[5] == "10:30" and package[7] == "":
                    truck1.add_package(package)
                    # add rest of packages not to exceed 16 on each truck
                if package[5] == "EOD" and package[7] == "":
                    if len(truck1.packages) < 16:
                        truck1.add_package(package)
                    elif len(truck2.packages) < 16:
                        truck2.add_package(package)
                    elif len(truck3.packages) < 16:
                        truck3.add_package(package)

    # # O(n) + O(1) so == O(n)
    # for entry in packages_hash.map:
    #     packages_by_address[entry[1][1]].append(entry[1])
    #
    # for key, value in packages_by_address.items():
    #     print(key, ' : ', value)
    #
    # # allocate packages based on priority and stipulations
    # # O(N^2)
    # for packages in packages_by_address.items():
    #     for individual_package in packages:
    #         if len(individual_package) > 0:
    #             # earliest deadline packages first
    #             print(individual_package)
    #             if individual_package[5] == "9:00":
    #                 truck1.add_package(individual_package)
    #             # next earliest deadline
    #             elif individual_package[5] == "9:05" or individual_package[7] == "Delayed---9:05":
    #                 truck2.add_package(packages)
    #             # next deadline time and stipulation to be delivered together
    #             elif individual_package[5] == "10:30" and "Must be delivered with" in individual_package[7]:
    #                 truck1.add_package(packages)
    #             # packages that have to go on truck 2
    #             elif individual_package[7] == "Can only be on truck 2":
    #                 truck2.add_package(packages)
    #             # packages that have this deadline but no special instructions
    #             elif individual_package[5] == "10:30" and individual_package[7] == "":
    #                 truck1.add_package(individual_package)
    #             # add rest of packages not to exceed 16 on each truck
    #             elif individual_package[5] == "EOD" and individual_package[7] == "":
    #                 if len(truck1.packages) < 16:
    #                     truck1.add_package(individual_package)
    #                 elif len(truck2.packages) < 16:
    #                     truck2.add_package(individual_package)
    #                 elif len(truck3.packages) < 16:
    #                     truck3.add_package(individual_package)


def get_best_route():
    print("best route")


truck1 = Truck()
truck2 = Truck()
truck3 = Truck()

# sort packages and allocate to trucks, need distance file for addresses
allocate_packages()
# determine routes for trucks based on algorithm
# get_best_route()

# truck1.build_delivery_list()
