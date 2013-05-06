import argparse, pickle, pprint, sys, random

from dijkstra_v1 import *
from dijkstra_v2 import *

n_step_value = 3
maxPathLength = 6
BIG = 1000000
maxRandomWeight = 10

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help="data file containing the graph")
    args = parser.parse_args(argv)

    graph = pickle.load(open(args.data, 'rb'))

    # We add the "dead ends" back into the original
    # graph (see below).
    de_graph = add_dead_ends_to_graph(graph)

    # Dijkstra's algorithm needs a weighted graph, so we make
    # one with unit weights
    unit_weighted_graph = make_unit_weighted_graph(de_graph)

    #random_weighted_graph = make_random_weighted_graph(de_graph, maxRandomWeight)

    # This is a dictionary with keys equal to wikipedia page titles
    # and values equal to the size of the n_step_set for that 
    # article
    graph_ns_size = nsize_dictionary(graph)

    sorted_graph = sorted(graph_ns_size.items(), key=lambda x:x[1])

    print "sorted_graph"
    pprint.pprint(sorted_graph)

    print "Size of sorted_graph: ", len(sorted_graph)

    cluster_centers = find_cluster_centers(graph, n_step_value)

    print "Cluster centers: "
    for c in cluster_centers:
        print c, graph_ns_size[c]

    # Will probably remove
    max_node, max_length = sorted_graph[-1]
    print max_node

    max_node_set = n_step_set(graph, max_node, 3, [])
    print max_node_set

    for dest_k, dest_v in graph.iteritems():
        if dest_k in max_node_set:
            print "Yes - ", dest_k.encode('ascii', 'ignore')
        else:
            print "No  - ", dest_k.encode('ascii', 'ignore')

    max_n_step_size = 0
    min_n_step_size = BIG
    for source_k, source_v in graph.iteritems():
        n_step_size = graph_ns_size[source_k]
        if n_step_size > max_n_step_size:
            max_n_step_size = n_step_size
        if n_step_size < min_n_step_size:
            min_n_step_size = n_step_size
        print n_step_size, n_step_set(graph, source_k, n_step_size, []), source_k.encode('ascii', 'ignore')
        sys.stdout.flush()

    print "min: ", min_n_step_size
    print "max: ", max_n_step_size

    parent_cluster = {}

    cluster_children = {}
    for cc in cluster_centers:
        cluster_children[cc] = []

    for source_k in de_graph:
        current_distance = sys.maxint
        for cc in cluster_centers:
            D, P = Dijkstra(unit_weighted_graph, cc, source_k)
            if source_k not in D:
                y = sys.maxint
            else:
                y = D[source_k]
            if y < current_distance:
                current_distance = y
                parent_cluster[source_k] = cc
        cluster_children[parent_cluster[source_k]].append(source_k)

    pprint.pprint(parent_cluster)

    pprint.pprint(cluster_children)

    D, P = Dijkstra(unit_weighted_graph,'7 for all Mankind', 'Jeans')
    print "D"
    print D

    print "P"
    print P

    print "after"

    sp = shortestPath(unit_weighted_graph,'7 for all Mankind', 'Jeans')
    print sp
    print "after sp"

# from http://www.python.org/doc/essays/graphs.html

def find_shortest_path(graph, start, end, path):
    if len(path) > maxPathLength:
        #print "long path:", len(path)
        #sys.stdout.flush()
        return None
    path = path + [start]
    if start == end:
        return path
    if not start in graph:
        return None
    shortest = None
    #print len(graph[start])
    #print path
    sys.stdout.flush()
    for node in graph[start]:
        if node not in path:
            newpath = find_shortest_path(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest

def nsize_dictionary(graph):
    graph_ns_size = {}
    for source_k, source_v in graph.iteritems():
        n_step = n_step_set(graph, source_k, 3, [])
        n_step_size = len(n_step)
        graph_ns_size[source_k] = n_step_size
    return graph_ns_size

def n_step_set(graph, start, n, n_set):
    #print n_set
    if n <= 0:
        return n_set
    if not start in graph:
        return n_set
    for node in graph[start]:
        if node not in n_set:
            n_set.append(node)
            n_set = n_step_set(graph, node, n-1, n_set)
    return n_set

def find_longest_path(graph, start, end, path):
    if len(path) > maxPathLength:
        print "long path:", len(path)
        sys.stdout.flush()
    path = path + [start]
    if start == end:
        #print path
        return path
    if not start in graph:
        return None
    if not end in graph:
        return None
    longest = None
    for node in graph[start]:
        if node not in path:
            newpath = find_longest_path(graph, node, end, path)
            if newpath:
                if not longest or len(newpath) > len(longest):
                    longest = newpath
    return longest

# source: http://stackoverflow.com/questions/8922060/breadth-first-search-trace-path
def bfs(graph, start, end):
    # maintain a queue of paths
    queue = []
    # push the first path into the queue
    queue.append([start])
    while queue:
        # get the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        # path found
        if node == end:
            return path
        if len(path) > maxPathLength:
            return None
        # enumerate all adjacent nodes, construct a new path and push it into the queue
        for adjacent in graph.get(node, []):
            new_path = list(path)
            new_path.append(adjacent)
            queue.append(new_path)

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

# Returns a list of the cluster centers.  These are the titles of
# articles with many links.  The cluster centers are not within n-step 
# reach of each other.
def find_cluster_centers(graph, n_step_value):

    # This is a dictionary with keys equal to wikipedia page titles
    # and values equal to the size of the n_step_set for that 
    # article.
    graph_ns_size = nsize_dictionary(graph)

    sorted_graph = sorted(graph_ns_size.items(), key=lambda x:x[1])

    # Start with an empty list
    cluster_centers = []
    for i in range(len(sorted_graph)):
        n, l = sorted_graph[-(i+1)]
        #print i, n.encode('ascii', 'ignore'), "links to ", l
        already_in = False
        for c in cluster_centers:
            if n in n_step_set(graph, c, n_step_value, []):
                # This node is already within reach of a node with more connections
                already_in = True
                #print n.encode('ascii', 'ignore'), " is ", n_step_value, "-reachable from cluster center ", c.encode('ascii', 'ignore')
        if not already_in:
            cluster_centers.append(n)
    return cluster_centers


if __name__ == "__main__":
    main()
