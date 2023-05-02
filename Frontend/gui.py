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
            # btree Visualization object (k = 3, key-width = 0.06, ref-width = 0.03, minNodeDistance = 0.1, nodesList[lowest level, ... , root], keysList)
            self.GraphNodes = bt.BTreeVisualization(3, 0.06, 0.03, 0.1, [6, 3, 1], [[1, 2], [7, 8, 9], [15], [33, 40], [50, 69, 70], [100], [4, 12], [41], [75, 76], [20]])
            # predefine 4 nodes 
            self.GraphNodes.calcNodesPositions()
            # calc where the references will be inside the nodes
            self.GraphNodes.calcRefPositions()
            # calc where the keys will be inside the nodes
            self.GraphNodes.calcKeyPositions()
            # calculate all graphs
            self.GraphNodes.assertValuesToGraphs()
            # draw all graphs
            #self.GraphNodes.drawTree()
            #temp += 1
            self.GraphNodes.runAnimation()
