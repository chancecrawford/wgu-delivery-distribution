import csv

from collections import defaultdict
from queue import PriorityQueue


# pull distance data from .csv and create graph with vertices based on locations
# contains algorithm for computing distances in graph
class DistanceGraph:
    # graph attributes
    def __init__(self, number_of_hubs):
        # use dictionary for graph ?
        self.vertices = number_of_hubs
        self.edges = [[-1 for i in range(number_of_hubs)] for j in range(number_of_hubs)]
        self.visited = []
        # self.deliveries = defaultdict(list)

    # need both vertices that form edge and distance between them
    def add_edge(self, first_vertex, second_vertex, distance_between):
        self.edges[first_vertex][second_vertex] = distance_between
        self.edges[second_vertex][first_vertex] = distance_between

    # def get_packages_for_delivery(self, packages):
    #     for row in packages:
    #         print('PfD Entry: ', row[1][1], row)
    #         self.deliveries[row[1][1]].append(row)

    # need a priority queue ?

    # pseudocode from course material for algorithm
    # def DijkstraShortestPath(startV):
    #
    #     for vertex currentV in graph:
    #         currentV->distance = Infinity
    #         currentV->predV = 0
    #         Push currentV to unvisitedQueue
    #
    #     # startV has a distance of 0 from itself
    #     startV->distance = 0
    #
    #     while (unvisitedQueue is not empty):
    #         # Visit vertex with minimum distance from startV
    #         currentV = PopMin unvisitedQueue
    #
    #     for vertex adjV adjacent to currentV:
    #         edgeWeight = weight of edge from currentV to adjV
    #         alternativePathDistance = currentV->distance + edgeWeight
    #
    #     # If shorter path from startV to adjV is found,
    #     # update adjV's distance and predecessor
    #     if (alternativePathDistance < adjV->distance):
    #         adjV->distance = alternativePathDistance
    #         adjV->predV = currentV

    def dijkstra(self, start_vertex):
        d = {v: float('inf') for v in range(self.vertices)}
        d[start_vertex] = 0

        priority_queue = PriorityQueue()
        priority_queue.put((0, start_vertex))

        while not priority_queue.empty():
            (dist, current_vertex) = priority_queue.get()
            self.visited.append(current_vertex)

            for neighbor in range(self.vertices):
                if self.edges[current_vertex][neighbor] != -1:
                    distance = self.edges[current_vertex][neighbor]
                    if neighbor not in self.visited:
                        old_cost = d[neighbor]
                        new_cost = d[current_vertex] + distance
                        if new_cost < old_cost:
                            priority_queue.put((new_cost, neighbor))
                            d[neighbor] = new_cost
        return d


# gets distance data from .csv
# O(N) for getting csv data
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
    distances = DistanceGraph(len(file_data))
    # populate graph with vertices using addresses
    for row in file_data:
        # create edges and add to graph
        # start at this index to pass over vertex, name, address
        for i in range(4, len(row)):
            # first vertex, second vertex, distance between two
            distances.add_edge(int(row[0]), int(file_data[i - 4][0]), float(row[i - 1]))
    return distances


distance_graph = create_distances_graph("data/WGUPS Distance Table.csv")
