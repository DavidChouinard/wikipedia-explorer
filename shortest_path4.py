from lib.graph import *
import io, argparse, pickle, pprint, sys

maxPathLength = 6
BIG = 1000000

def main(args):
    graph = pickle.load(open(args.data, 'rb'))
    pprint.pprint(graph)
    max_n_step_size = 0
    min_n_step_size = BIG
    for source_k, source_v in graph.iteritems():
        n_step = n_step_set(graph, source_k, 3, [])
        n_step_size = len(n_step)
        if n_step_size > max_n_step_size:
            max_n_step_size = n_step_size
        if n_step_size < min_n_step_size:
            min_n_step_size = n_step_size
        print n_step_size, n_step, source_k.encode('ascii', 'ignore')
        sys.stdout.flush()

    print "min: ", min_n_step_size
    print "max: ", max_n_step_size

    for source_k, source_v in graph.iteritems():
        print "here", source_k.encode('ascii', 'ignore'), len(n_step_set(graph, source_k, 1, []))
        for dest_k, dest_v in graph.iteritems():
            #sp = find_shortest_path(graph,source_k,dest_k,[])
            sp = bfs(graph,source_k,dest_k)
            if sp:
                print len(sp), sp, source_k.encode('ascii', 'ignore'), dest_k.encode('ascii', 'ignore')
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
    main(parser.parse_args())
