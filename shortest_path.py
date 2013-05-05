from lib.graph import *
import io, argparse, pickle, pprint, sys, random

from dijkstra_v1 import *
from dijkstra_v2 import *

maxPathLength = 6
BIG = 1000000
maxRandomWeight = 10

#graph = {'a': {'w': 14, 'x': 7, 'y': 9},
#            'b': {'w': 9, 'z': 6},
#            'w': {'a': 14, 'b': 9, 'y': 2},
#            'x': {'a': 7, 'y': 10, 'z': 15},
#            'y': {'a': 9, 'w': 2, 'x': 10, 'z': 11},
#            'z': {'b': 6, 'x': 15, 'y': 11}}

def main(args):
    graph = pickle.load(open(args.data, 'rb'))
    pprint.pprint(graph)

    de_graph = add_dead_ends_to_graph(graph)
    #pprint.pprint(de_graph)

    wgraph = make_unit_weighted_graph(de_graph)
    #pprint.pprint(wgraph)

    rgraph = make_random_weighted_graph(de_graph, maxRandomWeight)
    #pprint.pprint(rgraph)

#    graph_ns_size = nsize_dictionary(graph)


    graph_ns_size = {}
    for source_k, source_v in graph.iteritems():
        n_step = n_step_set(graph, source_k, 3, [])
        n_step_size = len(n_step)
        graph_ns_size[source_k] = n_step_size

    cluster_centers = []
    sorted_graph = sorted(graph_ns_size.items(), key=lambda x:x[1])

    for i in range(len(sorted_graph)):

        n, l = sorted_graph[-(i+1)]
        print i, n.encode('ascii', 'ignore'), l

        already_in = False
        for c in cluster_centers:
            if n in n_step_set(graph, c, 3, []):
                already_in = True
                print n.encode('ascii', 'ignore'), 
                " is n-reachable from cluster center ", c.encode('ascii', 'ignore')
        if not already_in:
            cluster_centers.append(n)

    sink_count = {}
    for source_k, source_v in graph.iteritems():
        for dest in source_v:
            if dest not in sink_count:
                sink_count[dest] = 1
            else:
                sink_count[dest] = sink_count[dest] + 1
    
    sorted_sink_count = sorted(sink_count.items(), key=lambda x:x[1])

    print "Sink counts: ", len(sink_count)
    for i in range(len(sorted_sink_count)):
        s, c = sorted_sink_count[-(i+1)]
        print i, s.encode('ascii', 'ignore'), c

    dead_ends = []
    for s in sink_count:
        if s not in graph:
            dead_ends.append(s)
        else:
            if graph[s] == set([]):
                dead_ends.append(s)

    print "Dead ends: ", len(dead_ends)    
    for d in dead_ends:
        print d.encode('ascii', 'ignore')

    print len(graph), len(cluster_centers)

    print "Cluster centers: "
    for c in cluster_centers:
        print c, graph_ns_size[c]


    max_node, max_length = sorted_graph[-1]
    print max_node

    max_node_set = n_step_set(graph, max_node, 3, [])
    print max_node_set

    for dest_k, dest_v in graph.iteritems():
        if dest_k in max_node_set:
            print "Yes - ", dest_k.encode('ascii', 'ignore')
        else:
            print "No  - ", dest_k.encode('ascii', 'ignore')

    for v in sorted_graph:
        print v
        

    max_n_step_size = 0
    min_n_step_size = BIG
    for source_k, source_v in graph.iteritems():
        n_step_size = graph_ns_size[source_k]
        if n_step_size > max_n_step_size:
            max_n_step_size = n_step_size
        if n_step_size < min_n_step_size:
            min_n_step_size = n_step_size
        print n_step_size, n_step, source_k.encode('ascii', 'ignore')
        sys.stdout.flush()

    print "min: ", min_n_step_size
    print "max: ", max_n_step_size

    for source_k, source_v in graph.iteritems():
        print "here - ", source_k.encode('ascii', 'ignore'), " - ", len(n_step_set(graph, source_k, 1, []))
        for dest_k, dest_v in graph.iteritems():
            print source_k.encode('ascii', 'ignore'), "->", dest_k.encode('ascii', 'ignore')
            sys.stdout.flush()
            #sp = find_shortest_path(graph,source_k,dest_k,[])
            sp = bfs(graph,source_k,dest_k)
            #sp_dijkstra = shortestPath(wgraph,source_k,dest_k)
            #sp_dijkstra = shortestpath(wgraph,source_k,dest_k)
            if sp:
                print len(sp), sp, ":", source_k.encode('ascii', 'ignore'), "->", dest_k.encode('ascii', 'ignore')
            sys.stdout.flush()
    #sp = find_shortest_path(graph,args.source,args.destination,[])
    #print "here", sp
    #if sp :
        #print len(sp)

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

# bfs found here : 
#   http://stackoverflow.com/questions/8922060/breadth-first-search-trace-path
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
        
def make_random_weighted_graph(graph, max_weight):
    weighted_graph = {}
    for node in graph:
        v = graph[node]
        weighted_graph[node] = {}
        for d in v:
            weighted_graph[node][d] = random.randint(1,max_weight)
    return weighted_graph
        
        
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help="data file containing the graph")
    parser.add_argument("source", help="source article title")
    parser.add_argument("destination", help="destination article title")
    main(parser.parse_args())
