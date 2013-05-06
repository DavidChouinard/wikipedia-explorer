# Given a specified graph, outputs the names of all the cluster centers
# prints the parent cluster for each title (node), and outputs the
# members of each cluster.

import argparse, pickle, pprint, sys, random

from dijkstra import *
from functions import *
from CONF import *

def main(args):
    graph = pickle.load(open(args.data, 'rb'))

    cluster_centers, cluster_members, parent_cluster = cluster_information(graph, n_step_value)

    print "Cluster center, size of n_step_set, size of cluster: "
    for c in cluster_centers:
        ns = n_step_set(graph, c, n_step_value, [])
        print "%s: %d, %d" % (c, len(ns), len(cluster_members[c]))

    print "\n"
    print "Parent cluster dictionary"
    pprint.pprint(parent_cluster)

    print "\n"
    print "Cluster members dictionary"
    pprint.pprint(cluster_members)

# Given a graph, cluster_information returns a 
# list of the cluster centers, a dictionary of cluster members, 
# and a dictionary of cluster parents.
def cluster_information(graph, n_step_value):
    # We add the "dead ends" back into the original
    # graph (see below).
    de_graph = add_dead_ends_to_graph(graph)

    # Dijkstra's algorithm needs a weighted graph, so we make
    # one with unit weights
    unit_weighted_graph = make_unit_weighted_graph(de_graph)

    #random_weighted_graph = make_random_weighted_graph(de_graph, maxRandomWeight)

    # This is a dictionary with keys equal to wikipedia page titles
    # and values equal to the size of the n_step_set for that 
    # article
    graph_ns_size = nsize_dictionary(graph)

    sorted_graph = sorted(graph_ns_size.items(), key=lambda x:x[1])

    cluster_centers = find_cluster_centers(graph, n_step_value)

    parent_cluster = {}

    cluster_members = {}
    for cc in cluster_centers:
        cluster_members[cc] = []

    for source_k in de_graph:
        current_distance = sys.maxint
        for cc in cluster_centers:
            D, P = Dijkstra(unit_weighted_graph, cc, source_k)
            if source_k not in D:
                y = sys.maxint
            else:
                y = D[source_k]
            if y < current_distance:
                current_distance = y
                parent_cluster[source_k] = cc
        cluster_members[parent_cluster[source_k]].append(source_k)

    return cluster_centers, cluster_members, parent_cluster

# Returns of dictionary of the size of the n_step_set for
# each title
def nsize_dictionary(graph):
    graph_ns_size = {}
    for source_k, source_v in graph.iteritems():
        n_step = n_step_set(graph, source_k, n_step_value, [])
        n_step_size = len(n_step)
        graph_ns_size[source_k] = n_step_size
    return graph_ns_size

# The set of articles that can be reached within 
# n steps of the node called start
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

# Returns a list of the cluster centers.  These are the titles of
# articles with many links.  The cluster centers are not within n-step 
# reach of each other.
def find_cluster_centers(graph, n_step_value):

    # This is a dictionary with keys equal to wikipedia page titles
    # and values equal to the size of the n_step_set for that 
    # article.
    graph_ns_size = nsize_dictionary(graph)

    sorted_graph = sorted(graph_ns_size.items(), key=lambda x:x[1])

    # Start with an empty list
    cluster_centers = []
    for i in range(len(sorted_graph)):
        n, l = sorted_graph[-(i+1)]
        #print i, n.encode('ascii', 'ignore'), "links to ", l
        already_in = False
        for c in cluster_centers:
            if n in n_step_set(graph, c, n_step_value, []):
                # This node is already within reach of a node with more connections
                already_in = True
                #print n.encode('ascii', 'ignore'), " is ", n_step_value, "-reachable from cluster center ", c.encode('ascii', 'ignore')
        if not already_in:
            cluster_centers.append(n)
    return cluster_centers


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help="data file containing the graph")
    main(parser.parse_args())
