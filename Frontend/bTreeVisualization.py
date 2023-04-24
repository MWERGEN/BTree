#   Created for BTree-MTT on 10.04.23
#
#   Creator: Tim Steiner
#
#   Task: 
#
#   Editors:
#       1.  Tim Steiner on 10.04.23
#       2.
#
###############################################
#
#   File description:
#       - visualization of the B-tree
#

import numpy as np
#from scipy.spatial import Delaunay
import igraph as ig
import matplotlib.pyplot as plt

class BTreeVisualization:

    # constructor
    def __init__(self, numNodes, k, keyWidth):
        # graph with Nodes (later surrounding keys and references of each node)
        self.gNodes = ig.Graph(numNodes)
        # graph with references inside the nodes
        self.gRefs = ig.Graph((2 * k + 1) * numNodes)
        # x-Positions of Nodes' centers
        self.xGNodes = []
        # y-Positions of Nodes' centers
        self.yGNodes = []
        # x-Positions of references
        self.xGRefs = []
        # y-Positions of references
        self.yGRefs = []
        # tree's definition of k (= minimum number of keys in node)
        self.k = k
        # key-width and ref-width
        self.keyWidth = keyWidth

    # add lists x and y to Nodes lists
    def addGNodeVis(self, x, y):
        # x-Positions of Nodes' centers (formal parameter list added to GNodes list)
        self.xGNodes = self.xGNodes + x
        # y-Positions of Nodes' centers (formal parameter list added to GNodes list)
        self.yGNodes = self.yGNodes + y

    # define the x- and y-Positions for the Graph's Nodes
    def assertValuesToGraphs(self):
        # for Nodes x
        self.gNodes.vs['x'] = self.xGNodes
        # for Nodes y
        self.gNodes.vs['y'] = self.yGNodes
        # for Refs x
        self.gRefs.vs['x'] = self.xGRefs
        # for Refs y
        self.gRefs.vs['y'] = self.yGRefs

    # calculates the x and y positions of all references
    def calcRefPositions(self):
        # iterate over all nodes' x positions 
        for i in self.xGNodes:
            # initialize a counter starting at -k
            ctr = (-1) * self.k
            # each node has 2k + 1 references (-k to k including 0)
            while ctr <= self.k:
                # each ref has a width of 0.06
                # adding k refs left from centre of node when i is negative
                # adding k refs right from centre of node when i is positive
                # adding 1 ref in the middle of the node
                self.xGRefs.append(i + (2 * self.keyWidth * ctr))
                # increment counter each iteration
                ctr += 1
        # iterate over all nodes' y positions
        for j in self.yGNodes:
            # initialize counter starting at 0
            ctr2 = 0
            # each node has 2k + 1 references (0 to 2k)
            while ctr2 <= 2 * self.k:
                # y position of each ref inside a specific node is equal to nodes y position
                self.yGRefs.append(j)
                # increment counter
                ctr2 += 1

    # draw whole tree including all part graphs
    def drawTree(self):
        # define automatic layout for Nodes Graph
        layoutNodes = self.gNodes.layout('auto')
        # define automatic layout for Refs Graph
        layoutRefs = self.gRefs.layout('auto')
        # simplify Nodes Graph
        self.gNodes.simplify()
        # simplify Refs Graph
        self.gRefs.simplify()
        # define subplot
        ax = plt.subplot()
        # set visual style
        visual_style = {}
        visual_style['vertex_shape'] = 'rectangle'
        # define Nodes-plot
        ig.plot(
            # nodes graph
            self.gNodes,
            # predefined layout
            layout = layoutNodes,
            # targetted subplot
            target = ax,
            # width of each node    = (2k nodes + 2k references + outer right reference)
            #                       = (2k * 2 + 1)    
            # width of one key or one reference is equal = 0.06                
            vertex_width = (2 * self.k * 2 + 1) * self.keyWidth,
            # choose height = width of one key to plot squares inside nodes
            vertex_height = self.keyWidth,
            vertex_size = 2, 
            # white color because nodes will be overlayed
            vertex_color = "white",
            # append style
            **visual_style
        )
        # define Refs-plot
        ig.plot(
            # refs graph
            self.gRefs,
            # predefined layout
            layout = layoutRefs,
            # targetted subplot
            target = ax,
            # width of ref is 0.06 -> we want squares  
            vertex_width = self.keyWidth,
            # height of ref is 0.06 -> we want squares  
            vertex_height = self.keyWidth,
            # gray color emblematic of refs
            vertex_color = "gray",
            # append style
            **visual_style
        )
        # plot graph
        plt.show()