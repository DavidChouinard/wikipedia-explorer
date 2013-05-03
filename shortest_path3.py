from lib.graph import *
import io, argparse, pickle, pprint, sys

maxPathLength = 10

def main(args):
    graph = pickle.load(open(args.data, 'rb'))
    #print len(graph)
    #pprint.pprint(graph)
    for source_k, source_v in graph.iteritems():
        print "Outer loop", source_k.encode('ascii', 'ignore')
        sys.stdout.flush()
        for dest_k, dest_v in graph.iteritems():
            print "Inner loop start", dest_k.encode('ascii', 'ignore')
            sys.stdout.flush()
            sp = find_shortest_path(graph,source_k,dest_k,[])
            lp = find_longest_path(graph,source_k,dest_k,[])
            print sp, lp, source_k.encode('ascii', 'ignore'), dest_k.encode('ascii', 'ignore')
            sys.stdout.flush()
            print "Inner loop finish", dest_k.encode('ascii', 'ignore')
            sys.stdout.flush()
    sp = find_shortest_path(graph,args.source,args.destination,[])
    print "here", sp
    if sp :
        print len(sp)

# from http://www.python.org/doc/essays/graphs.html

def find_shortest_path(graph, start, end, path):
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
    shortest = None
    print len(graph[start])
    print path
    sys.stdout.flush()
    for node in graph[start]:
        if node not in path:
            newpath = find_shortest_path(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help="data file containing the graph")
    parser.add_argument("source", help="source article title")
    parser.add_argument("destination", help="destination article title")
    main(parser.parse_args())
