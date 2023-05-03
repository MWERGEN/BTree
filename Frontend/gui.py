#   Created for BTree-MTT on 10.04.23
#
#   Creator: Tim Steiner
#
#   Task: 
#
#   Editors:
#       1.  Tim Steiner on 10.04.23
#       2.  Marius Wergen on 03.05.23
#
###############################################
#
#   File description:
#       - gui file
#
from Frontend import bTreeVisualization as bt

class Gui:
    
    # function for testing draw-behaviour of graph
    def drawGraph(self):
            # btree Visualization object (k = 3, key-width = 0.06, ref-width = 0.03, minNodeDistance = 0.1, nodesList[lowest level, ... , root], keysList, animation=moveKey)
            self.GraphNodes = bt.BTreeVisualization(3, 0.2, 0.03, 0.1, [6, 3, 1], [[1, 2], [7, 8, 9], [15], [33, 40], [50, 69, 70], [9999], [4, 12], [41], [75, 76], [20]], [[], [], [], [], [], [], [0, 1, 2], [3, 4], [5], [6, 7, 8]], 1)
            # predefine 4 nodes 
            self.GraphNodes.calcNodesPositions()
            # calc where the references will be inside the nodes
            self.GraphNodes.calcRefPositions()
            # calc where the keys will be inside the nodes
            self.GraphNodes.calcKeyPositions()
            # calculate all graphs
            self.GraphNodes.assertValuesToGraphs()
            # calculate the edges' relationships
            self.GraphNodes.calcEdges()
            # draw all graphs
            # TODO: animation 
            self.GraphNodes.runAnimation()
