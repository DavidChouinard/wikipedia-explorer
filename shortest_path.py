# -*- coding: utf-8 -*-

from lib.graph import *
import io, argparse, pickle

def main(args):
    graph = pickle.load(open(args.data, 'rb'))

    # TODO: Find the distance between args.source and args.destination

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help="data file containing the graph")
    parser.add_argument("source", help="source article title")
    parser.add_argument("destination", help="destination article title")
    main(parser.parse_args())
