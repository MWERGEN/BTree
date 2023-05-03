#   Created for BTree-MTT on 10.04.23
#
#   Creator: Tim Steiner
#
#   Tasks:  MBT-6
#
#   Editors:
#       1.  Tim Steiner on 10.04.23
#       2.  Marius Wergen on 27.04.23
#       3.  Marius Wergen on 02.05.23
#       4.  Marius Wergen on 03.05.23
#
###############################################
#
#   File description:
#       - visualization of the B-tree
#

import numpy as np
import math
import igraph as ig
import itertools as it
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# initialize the subplots where the graph will be displayed
# black background for design
fig, ax = plt.subplots(facecolor='black')
# configuration for subplot area in matplotlib-window:
#   -   left, bottom, right, top define where the edge of the subplot area is on the matplotlib-window
#           -> by this configuration, the graph is positioned on the border of the window
#           -> depending on its width to height ratio, the part of the window where no graph is plotted is drawn white
#              whereas the part of the window where the graph is plotted has a gray background
#   -   wspace, hspace define the space between multiple subplots
#           -> we just have one subplot so these values are irrelevant  
fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

class BTreeVisualization:

    # constructor
    def __init__(self, k, keyWidth, refWidth, minNodeDistance, nodesList, keysList, edgesList, currentAnimation):
        # save list of how many nodes are on each level of the tree
        self.nodesList = nodesList
        # save list of which keys are in which node
        self.keysList = keysList
        # safe edges in a List
        # format:       [[],     [],     [0, 1], ...]
        #   node         0       1         2
        #   edge to    none    none     node 0 and 1
        self.edgesList = edgesList
        # list containing all edges as tupels
        self.edgesListTupel = []
        # generate a List with all Labels (key-Values)
        # -> chaining all elements in the lists in keysList together
        self.keyLabels = list(it.chain.from_iterable(self.keysList))
        # make labels bold
        self.formatLabels()
        # calculate how many nodes the Graph has
        self.numOfNodes = self.calcNumOfNodes(nodesList)
        # calculate how many keys the Graph has
        self.numOfKeys = self.calcNumOfKeys(keysList)
        # graph with Nodes (later surrounding keys and references of each node)
        self.gNodes = ig.Graph(self.numOfNodes)
        # graph with references inside the nodes
        self.gRefs = ig.Graph((2 * k + 1) * self.numOfNodes)
        # graph with aid-structure for reference-edge-visualization
        self.gRefsAid = ig.Graph((2 * k + 1) * self.numOfNodes)
        # graph with keys inside the nodes
        self.gKeys = ig.Graph(self.numOfKeys)
        # key for moving animation
        self.gMovingKey = ig.Graph(1)
        # x-Positions of Nodes' centers
        self.xGNodes = []
        # y-Positions of Nodes' centers
        self.yGNodes = []
        # x-Positions of references
        self.xGRefs = []
        # y-Positions of references
        self.yGRefs = []
        # x-Positions of aid-structures for refs
        self.xGRefsAid = []
        # y-Positions of aid-structures for refs
        self.yGRefsAid = []
        # x-Positions of keys
        self.xGKeys = []
        # y-Positions of keys
        self.yGKeys = []
        # x-Positions of moving keys
        self.xGMovingKey = []
        # y-Positions of moving keys
        self.yGMovingKey = []
        # tree's definition of k (= minimum number of keys in node)
        self.k = k
        # key-width
        self.keyWidth = keyWidth
        # ref-width
        self.refWidth = refWidth
        # node width
        #   = (2k keys + 2k references + outer right reference)
        #   = (2k * (keyWidth + refWidth)) + refWidth
        self.nodeWidth = self.k * 2 * (self.keyWidth + self.refWidth) + self.refWidth
        # horizontal distance between the tree's leafs
        # -> distances between other nodes are higher
        self.minNodeDistance = minNodeDistance
        # declare visual style
        self.visual_style = {}
        # rectangular vertices
        self.visual_style['vertex_shape'] = 'rectangle'
        self.currentAnimation = currentAnimation
        self.x = [0]
        self.y = [1]
        self.i = 69

    # takes all labels and makes them bold
    def formatLabels(self):
        # list for temporarily saving the formatted labels
        tempLabels = []
        # iterate over all labels
        for i in self.keyLabels:
            # format each Label with a LaTex expression
            # expression makes the label bold
            tempLabels.append('$\\mathbf{' + str(i) + '}$')
        # update the labels-list with the formatted labels
        self.keyLabels = tempLabels

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
    
    # calculates how many keys the keysList has combined
    def calcNumOfKeys(self, keysList):
        # counts number of keys
        keyCtr = 0
        # iterates over keysList
        for i in keysList:
            # add the number of keys in every node to the counter
            keyCtr += len(i)
        # return total number of keys
        return keyCtr

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

    # calculates the x and y positions of all references
    def calcRefPositions(self):
        # iterate over all nodes' x positions 
        for i in self.xGNodes:
            # initialize a counter starting at -k
            ctr = (-1) * self.k
            # each node has 2k + 1 references (-k to k including 0)
            while ctr <= self.k:
                # each ref has a predefined widht (self.keyWidth)
                # adding k refs left from centre of node when i is negative
                # adding k refs right from centre of node when i is positive
                # adding 1 ref in the middle of the node
                self.xGRefs.append(i + ((self.refWidth + self.keyWidth) * ctr))
                # edges should stick on the center x-Pos of a reference
                self.xGRefsAid.append(i + ((self.refWidth + self.keyWidth) * ctr))
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
                # y position is the bottom of the ref in order to force the edges to stick at the bottom of a ref
                self.yGRefsAid.append(j - 2 * self.refWidth)
                # increment counter
                ctr2 += 1

    # calculates the x and y positions of all keys
    def calcKeyPositions(self):
        # counter which node is currently touched
        ctrNodes = 0
        # iterate over all nodes' x positions 
        for i in self.xGNodes:
            # the left outer key in a node is:
            #   ->  the centre of the node (i)
            #           minus (k - 1) key- and refWidths
            #           minus 0.5 key- and refWidths
            # this temp-variable will be raised by (keyWidth + refWidth) for the next key in the node
            nextKeyXPosition = i - (self.k - 0.5) * (self.keyWidth + self.refWidth)
            # iterate over all keys in the current node
            for j in self.keysList[ctrNodes]:
                # add the calculates x-Position for the key to the key-graph-list
                self.xGKeys.append(nextKeyXPosition)
                # the next key is one key-width and one ref-width right from the current x-position
                nextKeyXPosition += (self.keyWidth + self.refWidth)
            # increment node-counter because the next iteration of the for loop will be for the next node
            ctrNodes += 1
        # reset Node counter for the y-Positions
        ctrNodes = 0
        # iterate over all nodes' y positions
        for k in self.yGNodes:
            # add as many y positions as there are keys in one node
            for l in self.keysList[ctrNodes]:
                # y position of each key inside a specific node is equal to nodes y position
                self.yGKeys.append(k)
            # increment node-counter because the next iteration of the for loop will be for the next node
            ctrNodes += 1
    
    # calculates the ref to ref connection for all edges
    def calcEdges(self):
        # counter which node is worked on
        ctrNode = 0
        # iterate over all edges
        for i in self.edgesList:
            # only conside lists in edgesList that are not empty
            # empty list in edgesList means no edges for this node
            if i:
                # counter which ref inside the node is worked on
                ctrRef = 0
                # iterate over all edges for the considered node
                for j in i:
                    # calculate parent ref
                    #   the outer left reference in the bottom left node is ref 0
                    #       now we have to calculate which index the outer left reference in our node has
                    #       we are in node ctrNode with 2 * k + 1 refs per node
                    #       so the index of the outer left ref is: ctrNode * (2 * k + 1)
                    #   we have to add ctrRef to aim a specific reference in the node
                    parent = ctrNode * (2 * self.k + 1) + ctrRef
                    # calculate child ref
                    #   the outer left reference in the bottom left node is ref 0
                    #       now we have to calculate which index the outer left reference in the child node has
                    #       the child node has index j with 2 * k + 1 refs per node
                    #       so the index of the outer left ref is: j * (2 * k + 1)
                    #   we have to add k to aim the center reference in the child-node
                    child = j * (2 * self.k + 1) + self.k
                    # add edge = (parentRef, childRef) to edgesListTupel
                    self.edgesListTupel.append((parent, child))
                    # increment ctrRef to aim for the right next ref in the node for the following iteration
                    ctrRef += 1
            # increment ctrNode to observe the next node in the next iteration
            ctrNode += 1
        # after calculating all edges' relationships, 
        # add the edges to the graph of the references Aid structures
        self.gRefsAid.add_edges(self.edgesListTupel)

    # define the x- and y-Positions and potential labels for all Graphs
    def assertValuesToGraphs(self):
        # for Nodes x
        self.gNodes.vs['x'] = self.xGNodes
        # for Nodes y
        self.gNodes.vs['y'] = self.yGNodes
        # for Refs x
        self.gRefs.vs['x'] = self.xGRefs
        # for Refs y
        self.gRefs.vs['y'] = self.yGRefs
        # for aid x
        self.gRefsAid.vs['x'] = self.xGRefsAid
        # for aid y
        self.gRefsAid.vs['y'] = self.yGRefsAid
        # for Keys x
        self.gKeys.vs['x'] = self.xGKeys
        # for Keys y
        self.gKeys.vs['y'] = self.yGKeys
        # assert the labels (key-values) to the key-graph
        self.gKeys.vs['label'] = self.keyLabels

    def animation1(self, width, height):
        self.x[0] += 0.005
        self.y[0] += 0.005
        self.gMovingKey.vs['x'] = self.x
        self.gMovingKey.vs['y'] = self.y
        self.gMovingKey.vs['label'] = ['$\\mathbf{' + str(self.i) + '}$']
        ig.plot(
            # keys graph
            self.gMovingKey,
            # targetted subplot
            target = ax,
            # width of refs
            vertex_width = self.keyWidth,
            # choose height = width of 2 refs
            vertex_height = 4 * self.refWidth,
            # gray color emblematic of refs
            vertex_color = "lightblue",
            # set color of moving vertex to red
            vertex_frame_color="red",
            # formula for dynamically resizing the labels, so they are perfectly fitting into the node
            # width and height depend on the axes of the graph
            vertex_label_size = 0.92 * math.sqrt(width) * math.sqrt(height),
            # append style
            **self.visual_style, 
        )

    # draw whole tree including all part graphs
    def _update_graph(self, frame):
        # get the bounding box of the subplot in pixels
        bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        # get the width and height of the subplot in pixels
        width, height = bbox.width, bbox.height
        # Remove plot elements from the previous frame
        ax.clear()
        # background color for subplot area
        ax.set_facecolor('lightgray')
        # transparent color for vertex
        #vertex_color_transparent = [(0, 0, 0, 0) for i in range(self.gNodes.vcount())]
        # define Nodes-plot
        ig.plot(
            # nodes graph
            self.gNodes,
            # targetted subplot
            target = ax,
            # node Width (calculation in constructor)     
            vertex_width = self.nodeWidth,
            # choose height = width of 2 refs
            vertex_height = 4 * self.refWidth,
            # white color because nodes will be overlayed
            vertex_color = 'white',
            # appendself. style
            **self.visual_style
        )
        # define Refs-Aid-plot
        ig.plot(
            # refs graph
            self.gRefsAid,
            # targetted subplot
            target = ax,
            # width of refs aid = refWidth * 0.5
            # -> edges really stick in the centre of a ref
            vertex_width = 0.5 * self.refWidth,
            # choose height very low to force the edge to stick at the bottom of a ref
            vertex_height = 0.001 * self.refWidth,
            # gray color emblematic of refs
            vertex_color = "gray",
            # append style
            **self.visual_style
        )
        # define Refs-plot
        ig.plot(
            # refs graph
            self.gRefs,
            # targetted subplot
            target = ax,
            # width of refs
            vertex_width = self.refWidth,
            # choose height = width of 2 refs
            vertex_height = 4 * self.refWidth,
            # gray color emblematic of refs
            vertex_color = "gray",
            # append style
            **self.visual_style
        )
        # define Keys-plot
        ig.plot(
            # keys graph
            self.gKeys,
            # targetted subplot
            target = ax,
            # width of refs
            vertex_width = self.keyWidth,
            # choose height = width of 2 refs
            vertex_height = 4 * self.refWidth,
            # gray color emblematic of refs
            vertex_color = "lightblue",
            # formula for dynamically resizing the labels, so they are perfectly fitting into the node
            # width and height depend on the axes of the graph
            vertex_label_size = 0.92 * math.sqrt(width) * math.sqrt(height),
            # append style
            **self.visual_style, 
        )
        if self.currentAnimation == 1:
            self.animation1(width, height)
        # count all elements of the graph
        nhandles = 2 * (len(self.keyLabels) + len(self.x)) + len(self.xGNodes) + len(self.xGRefs) + len(self.xGRefsAid) + len(self.edgesListTupel)
        # choose all children from the graph to display the whole graph
        handles = ax.get_children()[:nhandles]
        # return elements to be displayed
        return handles
        
    # run the graph-animation
    def runAnimation(self):
        # define animation
        # animation on the figure
        # updating function is _update_graph
        # blitting (blit) improves the fading for the animation
        ani = animation.FuncAnimation(fig, self._update_graph, interval=1, blit=True)
        # show the plot
        plt.show()
