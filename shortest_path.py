# Finds shortest path between the specified source and destination nodes
# Uses breadth-first search (BFS), Dijkstra's algorithm, or a naive algorithm
# Returns a list that is the sequence of titles of nodes in the path
# Returns empty list if there is no path.

import argparse, pickle, pprint, sys, random

from dijkstra import *
from functions import *
from CONF import *

def main(args):

    # If both args.d and args.n are false, use DFS
    # If args.n is true, use naive
    # If args.d is true, use Dijkstra
    # If args.b is true, use BFS

    source_k = args.source
    dest_k = args.destination

    graph = pickle.load(open(args.data, 'rb'))

    de_graph = add_dead_ends_to_graph(graph)

    wgraph = make_unit_weighted_graph(graph)
    #pprint.pprint(wgraph)

    rgraph = make_random_weighted_graph(de_graph, maxRandomWeight)
    #pprint.pprint(rgraph)

    if source_k not in de_graph:
        print "start node not in graph"
    elif dest_k not in de_graph:
        print "end node not in graph"
    else:
        if args.n:
            print "Naive"
            sp = find_shortest_path(graph,source_k,dest_k,[])
        elif args.d:
            print "Dijkstra"
            sp = shortestPath(wgraph,source_k, dest_k)
        else:
            print "BFS"
            sp = bfs(graph,source_k, dest_k)

        if sp:
            print len(sp)-1, sp, ":", source_k.encode('ascii', 'ignore'), "->", dest_k.encode('ascii', 'ignore')
        else:
            print "path does not exist."
    


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help="data file containing the graph")
    parser.add_argument("source", help="source article title")
    parser.add_argument("destination", help="destination article title")
    parser.add_argument('-n', action='store_true', default=False, help="use naive algorithm")
    parser.add_argument('-b', action='store_true', default=False, help="use BFS algorithm")
    parser.add_argument('-d', action='store_true', default=False, help="use Dijkstra's algorithm")
    main(parser.parse_args())
