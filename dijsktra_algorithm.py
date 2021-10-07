from distances import DistanceGraph

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
