# -*- coding: utf-8 -*-

from lib.graph import *
import io, argparse, pickle, pprint
graph = None

def main(args):
    global graph
    depth = int(args.destination)
    graph = pickle.load(open(args.data, 'rb'))
    pprint.pprint(graph)
    # TODO: Find the distance between args.source and args.destination
    printstring(args.source,depth)
   # for article in graph[args.source]:
    #    for art2 in graph[article]:
     #       print art2

def printstring(string,depth):
    for art in graph[string]:
        if depth >= 0:  
            print art
        else:
            printstring(string,depth - 1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help="data file containing the graph")
    parser.add_argument("source", help="source article title")
    parser.add_argument("destination", help="destination article title")
    main(parser.parse_args())
