# Given a graph, prints paths between all source, destination pairsa
import argparse, pickle, pprint, sys, random
from dijkstra import *
from functions import *
from bfs import *
from naive import *
from CONF import *

def main(args):

    # If both args.d and args.n are false, use BFS
    # If args.n is true, use naive
    # If args.d is true, use Dijkstra
    # If args.b is true, use BFS

    graph = pickle.load(open(args.data, 'rb'))

    de_graph = add_dead_ends_to_graph(graph)

    unit_weighted_graph = make_unit_weighted_graph(graph)

    for source_k, source_v in graph.iteritems():
        print source_k.encode('ascii', 'ignore')
        for dest_k, dest_v in graph.iteritems():
            if args.d:
                # use Dijkstra's algorithm
                sp = shortestPath(unit_weighted_graph,source_k,dest_k)
            elif args.n:
                # use naive algorithm
                sp = find_shortest_path(graph,source_k,dest_k,[])
            else:
                # use BFS algorithm
                sp = bfs(graph,source_k,dest_k)
            if sp and len(sp) > 1:
                print len(sp)-1, sp, ":", source_k.encode('ascii', 'ignore'), "->", dest_k.encode('ascii', 'ignore')



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help="data file containing the graph")
    parser.add_argument('-n', action='store_true', default=False, help="use naive algorithm")
    parser.add_argument('-b', action='store_true', default=False, help="use BFS algorithm")
    parser.add_argument('-d', action='store_true', default=False, help="use Dijkstra's algorithm")
    main(parser.parse_args())
