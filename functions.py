import random

# Returns a list of nodes that are the destination
# from some link in the original adjacency list
# graph but which were not included as nodes in 
# that original graph
# It does this by first making a dictionary of all
# destinations.  The keys are the number of links to
# the destinations.
def find_dead_ends(graph):
    sink_count = {}
    for source_k, source_v in graph.iteritems():
        for dest in source_v:
            if dest not in sink_count:
                sink_count[dest] = 1
            else:
                sink_count[dest] = sink_count[dest] + 1

    dead_ends = []
    for s in sink_count:
        if s not in graph:
            dead_ends.append(s)
        else:
            if graph[s] == set():
                dead_ends.append(s)
    return dead_ends

# Add the leaf nodes to graph, using unweighted list
# This is the original graph format
def add_dead_ends_to_graph(graph):
    dead_ends = find_dead_ends(graph)
    for de in dead_ends:
        graph[de] = set([])
    return graph

# Change adjacency list representation to dictionary
# and add unit weights
def make_unit_weighted_graph(graph):
    weighted_graph = {}
    for node in graph:
        v = graph[node]
        weighted_graph[node] = {}
        for d in v:
            weighted_graph[node][d] = 1
    return weighted_graph
        
# Change adjacency list representation to dictionary
# and add unit weights
def make_random_weighted_graph(graph, max_weight):
    weighted_graph = {}
    for node in graph:
        v = graph[node]
        weighted_graph[node] = {}
        for d in v:
            weighted_graph[node][d] = random.randint(1,max_weight)
    return weighted_graph
