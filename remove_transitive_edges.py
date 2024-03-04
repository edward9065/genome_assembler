#!/usr/bin/env python

"""
    usage:
        remove_transitive_edges [options] graph.dot
    where the options are:
        -h,--help : print usage and quit

    graph.dot is a file with a directed graph. The first row is always
        
        Digraph G {

    and the last row is always 

        }

    Each row in the middle section describes an edge. For example,

        1 -> 2

    is a directed edge from a node with the label '1' to the node with the label    '2'.
"""

from sys import argv, stderr
from getopt import getopt, GetoptError
from copy import deepcopy
from graph import *

def DFS_visit(G, node, nodes_color, reverse_ordered_nodes):
    nodes_color[node] = 1
    for node2 in G.edges[node].keys():
        if nodes_color[node2] == 0:
            DFS_visit(G, node2, nodes_color, reverse_ordered_nodes)
    nodes_color[node] = 2
    reverse_ordered_nodes.append(node)

def simplify(G):
    """Simplify the graph S by removing the transitively-inferrible edges.

    S is just a copy of G, which is the input to the graph. 
    """

    nodes = G.nodes()
    nodes_color = dict.fromkeys(nodes, 0)
    reverse_ordered_nodes = []

    for node in nodes:
        if nodes_color[node] == 0:
            DFS_visit(G, node, nodes_color, reverse_ordered_nodes)
    edges = {}
    for i in range(len(reverse_ordered_nodes)-1, 0, -1):
        edges[reverse_ordered_nodes[i]] = {reverse_ordered_nodes[i-1]: 1}
    return Graph(edges)

def main(filename):
    # read the graph from the input file
    graph = Graph(filename)
    print(f"Read the graph from {filename}", file=stderr)

    # simplify the graph by removing the transitively-inferrible edges
    simplified = simplify(graph)
    print(f"Simplified the graph", file=stderr)

    # print the simplified graph in the same format as the input file
    print(simplified)

if __name__ == "__main__":
    try:
        opts, args = getopt(argv[1:], "h", ["help"])
    except GetoptError as err:
        print(err)
        print(__doc__, file=stderr)
        exit(1) 

    for o, a in opts:
        if o in ("-h", "--help"):
            print(__doc__, file=stderr)
            exit()
        else:
            assert False, "unhandled option"

    if len(args) != 1:
        print(__doc__, file=stderr)
        exit(2)

    main(args[0])
