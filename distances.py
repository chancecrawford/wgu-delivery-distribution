import csv

from queue import PriorityQueue


# pull distance data from .csv and create graph with vertices based on locations
# contains algorithm for computing distances in graph
class DistanceGraph:
    # graph attributes
    def __init__(self):
        self.vertices = []
        self.edges = {}
        self.visited = []

    # need both vertices that form edge and distance between them
    def add_edge(self, first_vertex, second_vertex, distance_between):
        # initialize entries in dict before adding elements there
        if first_vertex not in self.edges:
            self.edges[first_vertex] = {}
        if second_vertex not in self.edges:
            self.edges[second_vertex] = {}
        # create edge pairs and distances for given addresses
        self.edges[first_vertex][second_vertex] = distance_between
        self.edges[second_vertex][first_vertex] = distance_between

    # takes two points, finds shortest path to all points from current one,
    # and returns shortest path distance for next vertex
    # O(ElogV) where E = # of edges and V = number of vertices
    def dijkstra(self, start_vertex, next_vertex):
        # create dictionary with address as key and infinite as initial distance from start vertex to that address
        d = {v: float('inf') for v in self.vertices}
        # set distance to itself as 0
        d[start_vertex] = 0
        # create pq and initialize with starting point
        priority_queue = PriorityQueue()
        priority_queue.put((0, start_vertex))

        while not priority_queue.empty():
            (dist, current_vertex) = priority_queue.get()
            # need to clear visited nodes before adding current one
            self.visited.clear()
            self.visited.append(current_vertex)
            # loop through addresses
            for neighbor in self.vertices:
                # make sure distance between current address and neighbor exist
                if self.edges[current_vertex][neighbor] != -1:
                    # set distance for comparison
                    distance = self.edges[current_vertex][neighbor]
                    if neighbor not in self.visited:
                        old_cost = d[neighbor]
                        new_cost = d[current_vertex] + distance
                        if new_cost < old_cost:
                            priority_queue.put((new_cost, neighbor))
                            d[neighbor] = new_cost
        if next_vertex is not None:
            return next_vertex, d[next_vertex]


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


distance_graph = create_distances_graph("data/WGUPS Distance Table.csv")
