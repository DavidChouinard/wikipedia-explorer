from lib.graph import *
import io, argparse, pickle, pprint

def main(args):
    graph = pickle.load(open(args.data, 'rb'))
    #pprint.pprint(graph)
    for source_k, source_v in graph.iteritems():
        for dest_k, dest_v in graph.iteritems():
            sp = find_shortest_path(graph,source_k,dest_k,[])
            print sp
    sp = find_shortest_path(graph,args.source,args.destination,[])
    print sp
    if sp :
        print len(sp)

# from http://www.python.org/doc/essays/graphs.html

def find_shortest_path(graph, start, end, path):
    path = path + [start]
    if start == end:
        #print path
        return path
    if not start in graph:
        return None
    shortest = None
    for node in graph[start]:
        if node not in path:
            newpath = find_shortest_path(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    # pprint.pprint(shortest)
    return shortest

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help="data file containing the graph")
    parser.add_argument("source", help="source article title")
    parser.add_argument("destination", help="destination article title")
    main(parser.parse_args())
