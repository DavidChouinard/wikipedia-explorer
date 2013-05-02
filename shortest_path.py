# -*- coding: utf-8 -*-

from lib.graph import *
import io, argparse, pickle

def main(args):
    graph = pickle.load(open(args.data, 'rb'))

    #head = graph.head
    #head.data["distance"] = 0
    #head.data["visited"] = True

    current_distance = 0
    for child in head.adjacent:
        child.data["distance"] = current_distance + 1
        
    # if "distance" in child.data
    
    # nodes have data and a list called adjacent

    for child in head.adjacent:
        print child.data
        

    # TODO: Find the distance between args.source and args.destination
    print args.source, args.destination

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help="data file containing the graph")
    parser.add_argument("source", help="source article title")
    parser.add_argument("destination", help="destination article title")
    main(parser.parse_args())
