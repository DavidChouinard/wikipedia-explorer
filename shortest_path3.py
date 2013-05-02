from lib.graph import *
import io, argparse, pickle, pprint

def main(args):
    graph = pickle.load(open(args.data, 'rb'))
   # pprint.pprint(graph)
   # for source_k, source_v 
   # sp = find_shortest_path(graph,args.source,args.destination,[])
  #  print sp
   # if sp: 
    #   print len(sp)
  #  lp = find_longest_path(graph,args.source,args.destination,[])
  #  print lp
  #  if lp: 
  #     print len(lp)
    bfs = bfs(graph,args.source,args.destination)
    print bfs
    if bfs:
        print len(bfs)

# adopted from http://www.python.org/doc/essays/graphs.html

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
        # enumerate all adjacent nodes, construct a new path and push it into the queue
        for adjacent in graph.get(node, []):
            new_path = list(path)
            new_path.append(adjacent)
            queue.append(new_path)


def find_reach(graph, start, reach)
    for node in graph[start]
    


def find_shortest_path(graph, start, end, reach):
    path = path + [start]
    if start == end:
       # print path
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
    return shortest

def find_shortest_path(graph, start, end, path):
    path = path + [start]
    if start == end:
       # print path
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
    return shortest

def find_shortest_path(graph, start, end, path):
    path = path + [start]
    if start == end:
       # print path
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
    return shortest

def find_longest_path(graph, start, end, path):
    path = path + [start]
    if start == end:
       # print path
        return path
    if not start in graph:
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
