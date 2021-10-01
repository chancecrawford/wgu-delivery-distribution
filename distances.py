import csv


# pull distance data from .csv and create graph with vertices based on locations
# contains algorithm for computing distances in graph
class DistanceGraph:
    # graph attributes
    def __init__(self, number_of_hubs):
        # use dictionary for graph ?
        self.vertices = number_of_hubs
        self.edges = [[-1 for i in range(number_of_hubs)] for j in range(number_of_hubs)]
        self.visited = []

    # need both vertices that form edge and distance between them
    def add_edge(self, first_vertex, second_vertex, distance_between):
        print("1st: ", first_vertex, ' 2nd: ', second_vertex, ' Weight: ', distance_between)
        self.edges[first_vertex][second_vertex] = distance_between
        self.edges[second_vertex][first_vertex] = distance_between


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


graph = create_distances_graph("WGUPS Distance Table.csv")
