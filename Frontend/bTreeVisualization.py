#   Created for BTree-MTT on 10.04.23
#
#   Creator: Tim Steiner
#
#   Tasks:  MBT-6
#
#   Editors:
#       1.  Tim Steiner on 10.04.23
#       2.  Marius Wergen on 27.04.23
#
###############################################
#
#   File description:
#       - visualization of the B-tree
#

import numpy as np
import igraph as ig
import matplotlib.pyplot as plt

# configuration for subplot area in matplotlib-window:
#   -   left, bottom, right, top define where the edge of the subplot area is on the matplotlib-window
#           -> by this configuration, the graph is positioned on the border of the window
#           -> depending on its width to height ratio, the part of the window where no graph is plotted is drawn white
#              whereas the part of the window where the graph is plotted has a gray background
#   -   wspace, hspace define the space between multiple subplots
#           -> we just have one subplot so these values are irrelevant  
plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

class BTreeVisualization:

    # constructor
    def __init__(self, k, keyWidth, minNodeDistance, nodesList):
        # save list of how many nodes are on each level of the tree
        self.nodesList = nodesList
        # calculate how many nodes the Graph has
        self.numOfNodes = self.calcNumOfNodes(nodesList)
        # graph with Nodes (later surrounding keys and references of each node)
        self.gNodes = ig.Graph(self.numOfNodes)
        # graph with references inside the nodes
        self.gRefs = ig.Graph((2 * k + 1) * self.numOfNodes)
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
        # key-width and 2 * ref-width
        self.keyWidth = keyWidth
        # node width
        #   = (2k nodes + 2k references + outer right reference)
        #   = (2k * 1.5 + 0.5)    
        #   (width of one key = width of 2 references)  
        self.nodeWidth = (1.5 * self.k * 2 + 0.5) * self.keyWidth
        # horizontal distance between the tree's leafs
        # -> distances between other nodes are higher
        self.minNodeDistance = minNodeDistance

    # calculates how many nodes the nodesList has combined
    def calcNumOfNodes(self, nodesList):
        # counts number of nodes
        nodeCtr = 0
        # iterates over nodesList
        for i in nodesList:
            # nodesList's elements are the number of nodes on a specific level = i
            # so we count the numbers of nodes on each level together
            nodeCtr += i
        # return total number of nodes in nodesList
        return nodeCtr

    # calc the x and y positions of all nodes
    # we start on the lowest level (leafs) and work upwards
    # and work from left to right for each level
    def calcNodesPositions(self):
        # counter for tree level
        # lower level (leafs) = level 1
        ctrLevel = 1
        # iterate over nodesList
        for i in self.nodesList:
            # number of nodes on level is equal
            if (i % 2 == 0):
                # counter for node position on level
                # example: 4 nodes on a level
                #   nodes:  |node1|   |node2|   |node3|   |node4|
                #   ------------------------------------------------
                #   ctrEven   -3        -1         1         3 
                ctrEven = (-1) * (i - 1)
                # calculate all nodes' positions
                # in our example: -3, -1, 1, 3(= 4-1)
                while ctrEven <= (i - 1):
                    # save x-Position 
                    # fixed point for calculation is (0,0)
                    # the distance from (0,0) to the node rigth/left from the centre is
                    # half the width of a node + half the distance between two nodes
                    # let's call this distance d
                    # the distance to the next node from there on is 2 * d (-> thats why we raise ctrEven later by two)
                    # multiplication with ctrLevel is for dynamic distance
                    # -> the higher the level, the more distance is needed
                    self.xGNodes.append(0.5 * ctrLevel * (self.nodeWidth + self.minNodeDistance) * ctrEven)
                    # save same y-Position for all nodes on one level
                    self.yGNodes.append(ctrLevel)
                    # distance to next node is 2 * d (watch above)
                    ctrEven += 2
            # number of nodes on level is NOT equal
            else:
                # counter for node position on level
                # example: 5 nodes on a level
                #   nodes:  |node1|   |node2|   |node3|   |node4|   |node5|
                #   ---------------------------------------------------------
                #   ctrOdd   -2        -1         0         2         3
                ctrOdd = (i - 1) * (-0.5)
                # calculate all nodes' positions
                # indeces in our example: -2, -1, 0, 1, 2(= (5-1)*1/2 )
                while ctrOdd <= (i - 1) * (0.5):
                    # save x-Position 
                    # fixed point for calculation is (0,0)
                    # the distance from (0,0) to the node rigth/left from the centre is
                    # the width of a node + the distance between two nodes
                    # let's call this distance d
                    # the distance to the next node from there on is d (-> thats why we raise ctrEven later by one)
                    # multiplication with ctrLevel is for dynamic distance
                    # -> the higher the level, the more distance is needed
                    self.xGNodes.append(ctrLevel * (self.nodeWidth + self.minNodeDistance) * ctrOdd)
                    # save same y-Position for all nodes on one level
                    self.yGNodes.append(ctrLevel)
                    # distance to next node is d (watch above)
                    ctrOdd += 1
            # the next element in nodesList describes the number of nodes on the upper level
            # -> so the level has to be incremented
            ctrLevel += 1

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
                # each ref has a width of 1/2 * keyWidth
                # adding k refs left from centre of node when i is negative
                # adding k refs right from centre of node when i is positive
                # adding 1 ref in the middle of the node
                self.xGRefs.append(i + (1.5 * self.keyWidth * ctr))
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
        # background color for subplot area
        ax.set_facecolor('lightgray')
        # set visual style
        visual_style = {}
        visual_style['vertex_shape'] = 'rectangle'
        # define Nodes-plot
        ig.plot(
            # nodes graph
            self.gNodes,
            # predefined layout
            # layout = layoutNodes,
            # targetted subplot
            target = ax,
            # node Width (calculation in constructor)     
            vertex_width = self.nodeWidth,
            # choose height = width of one key to plot squares inside nodes
            vertex_height = self.keyWidth,
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
            # width of refs
            vertex_width = 0.5 * self.keyWidth,
            # height of refs
            vertex_height = self.keyWidth,
            # gray color emblematic of refs
            vertex_color = "gray",
            # append style
            **visual_style
        )
        # plot graph
        plt.show()