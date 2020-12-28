  
#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# File    : draw_graph.py
# Author  : Wang Zehao
# Email   :
# Date    : Dec 28 2020
#
# Distributed under the MIT license

"""
These are tools for plot graph data
"""

import matplotlib
def rgba2hex(R, G, B, A):
    """ All should be float between 0-1"""
    return matplotlib.colors.to_hex([ R, G, B, A ], keep_alpha=True)

colormap = {
    'green' : [0.051, 0.671, 0.384],
    'red' : [0.878, 0.29, 0.247],
    'blue': [0.529, 0.808, 0.98],
}

from graphviz import Digraph
def nx2styleddot(networkxG, start_nodes, end_nodes, out_file, description='', format='pdf'):
    """
    This function draw start node, end node and the whole path in KG. The input graph object is networkx MultiDiGraph
    """
    f = Digraph(comment=description, filename=out_file, format=format) # handle well for parallel edges
    f.attr(rankdir='LR') # horizontal display
    for node in networkxG.nodes:
        if node in start_nodes:
            color = 'green'
        elif node in end_nodes:
            color= 'red'
        else:
            color= 'blue'
        f.node(node, label=node, style='filled', color=rgba2hex(*colormap[color], 0.5))
    for edge in networkxG.edges:
        f.edge(edge[0], edge[1], label=edge[2])
    
    return f
