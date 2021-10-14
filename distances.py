# Chance Crawford --- Student ID:

import csv


# pull distance data from .csv and create graph with vertices based on locations
# contains algorithm for computing distances in graph
class DistanceGraph:
    # graph attributes
    def __init__(self):
        self.vertices = []
        self.edges = {}
        self.visited = []

    # need both vertices that form edge and distance between them
    # O(1) since we check at key before insertion
    def add_edge(self, first_vertex, second_vertex, distance_between):
        # initialize entries in dict before adding elements there
        if first_vertex not in self.edges:
            self.edges[first_vertex] = {}
        if second_vertex not in self.edges:
            self.edges[second_vertex] = {}
        # create edge pairs and distances for given addresses
        self.edges[first_vertex][second_vertex] = distance_between
        self.edges[second_vertex][first_vertex] = distance_between

    # takes in route to optimize, loops through addresses in route to find best route
    # from current address to next address in route
    # O(N^2)
    def get_shortest_path(self, original_route):
        # set home delivery hub as first address
        optimized_route = ["4001 South 700 East"]

        # loop through addresses in route to determine shortest route
        # removes address after getting best route to next address and breaks out of loop when none left
        while len(original_route) != 0:
            # set starting point with distance to itself
            best_route = [0, "4001 South 700 East"]
            for address in original_route:
                # get distances between locations
                distance = self.edges[optimized_route[-1]][address]
                # handle multiple packages at same address
                if best_route[0] == 0:
                    best_route = [distance, address]
                # if shorter distance found, set as new route
                if distance < best_route[0] and distance != 0:
                    best_route = [distance, address]
            # add shortest route to optimized route
            if best_route[1] not in optimized_route:
                optimized_route.append(best_route[1])
            # remove route to avoid any accidental loops over same address
            original_route.remove(best_route[1])

        return optimized_route


# gets distance data from .csv
# O(1) for getting csv data and for appending data
def retrieve_distance_data(distances_file):
    # initialize array for getting csv data
    file_data = []
    # use csv reader to get data
    with open(distances_file) as file:
        reader = csv.reader(file)
        # skip first row
        next(reader, None)
        # insert each row into hashmap
        for row in reader:
            file_data.append(row)
    return file_data


# create graph for determining best routes
# want this modularized in case we need to determine best route with multiple distance files
# O(N^2) for populating graph
def create_distances_graph(file):
    # get data from csv
    file_data = retrieve_distance_data(file)
    # initialize graph to size of file data
    distances = DistanceGraph()
    # populate graph with vertices using addresses
    for row in file_data:
        # create edges and add to graph
        # start at this index to pass over vertex, name, address
        for i in range(3, len(row)):
            # first vertex, second vertex, distance between two
            distances.add_edge(row[1], file_data[i - 3][1], float(row[i - 1]))
        # add address to vertices for comparison in distance algorithm
        distances.vertices.append(row[1])
    return distances


# create graph from file
distance_graph = create_distances_graph("data/WGUPS Distance Table.csv")
