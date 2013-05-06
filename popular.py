# Returns the n most linked-to articles in the graph
# example: 
# python popular.py data/jeans.pkl

import argparse, pickle, pprint
from CONF import *

def main(args):
    # number of popular articles requested is in args.size, default is 10
    graph = pickle.load(open(args.data, 'rb'))

    sink_count = {}
    for source_k, source_v in graph.iteritems():
        for dest in source_v:
            if dest not in sink_count:
                sink_count[dest] = 1
            else:
                sink_count[dest] = sink_count[dest] + 1
    
    sorted_sink_count = sorted(sink_count.items(), key=lambda x:x[1])

    print "# Title, number of nodes that connect to this article"
    for i in range(int(args.size)):
        s, c = sorted_sink_count[-(i+1)]
        print s.encode('ascii', 'ignore'), c

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help="data file containing the graph")
    parser.add_argument('size', nargs='?', default=10, help="number of popular articles to return")
    main(parser.parse_args())
