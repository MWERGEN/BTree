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
#       - gui file
#
from Frontend import bTreeVisualization as bt

class Gui:
    # TODO implement mainloop

    #define main loop
    #def mainFuntion():
        # while True: 
            # do stuff

    # function for testing draw-behaviour of graph
    def drawGraphTest(self):
        # btree Visualization object (4 nodes, k = 3, key-width = 0.06)
        self.GraphNodes = bt.BTreeVisualization(4, 3, 0.06)
        # predefine 4 nodes 
        self.GraphNodes.addGNodeVis([0.82, 0, 0.82, 1.64], [0, -0.5, -0.5, -0.5])
        # calc where the references will be inside the nodes
        self.GraphNodes.calcRefPositions()
        # calculate all graphs
        self.GraphNodes.assertValuesToGraphs()
        # draw all graphs
        self.GraphNodes.drawTree()
