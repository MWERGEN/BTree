#   Created for BTree-MTT on 10.04.23
#
#   Creator: Tim Steiner
#
#   Task: 
#
#   Editors:
#       1.  Tim Steiner on 10.04.23
#       2.  Marius Wergen on 03.05.23
#       3.  Marius Wergen on 04.05.23
#
###############################################
#
#   File description:
#       - gui file
#

from Frontend import bTreeVisualization as bt

from Frontend import anim as ani

class Gui:
    
    # function for testing draw-behaviour of graph
    def drawGraph(self):
            
            #animTypeList = [1, 1, 0]
            #treeList = [[[6, 3, 1], [[1, 2], [7, 8, 9], [7, 8, 11], [33, 40], [50, 69, 70], [500], [4, 6, 12, 24, 30, 40], [41], [9999], [20, 25]], [[], [], [], [], [], [], [0, 1, 2], [3, 4], [5], [6, 7, 8]]], [[6, 3, 1], [[1, 2], [7, 8, 9], [7, 8, 11], [33, 40], [50, 69, 70], [500], [4, 6, 12, 24, 30, 40], [41], [9999], [20, 25]], [[], [], [], [], [], [], [0, 1, 2], [3, 4], [5], [6, 7, 8]]], [[6, 3, 1], [[1, 2], [7, 8, 9], [7, 8, 11], [33, 40], [50, 69, 70], [500], [4, 6, 12, 24, 30, 40], [41], [9999], [10, 20, 25]], [[], [], [], [], [], [], [0, 1, 2], [3, 4], [5], [6, 7, 8]]]]
            # für ref liste:    0. ist egal, da der an festem Punkt (neben root) startet
            #                   1. ist die posi wo er an der root startet
            #                   2. ist posi wo er an erstem inneren startet zum blatt hin
            #operands = [[9, 9, 6], [9, 6, 9], [0, 0, 2], [10, 10, 12]]
            ####
            # no. 1
            # input when leaf full
            #animTypeList = [1, 1, 1, 0]
            #treeList = [[[4, 1], [[1, 2, 3], [5, 6, 7, 8, 9, 11], [15, 20, 25], [70, 80, 90, 100], [4, 12, 35]], [[], [], [], [], [0, 1, 2, 3]]], [[4, 1], [[1, 2, 3], [5, 6, 7, 8, 9, 11], [15, 20, 25], [70, 80, 90, 100], [4, 12, 35]], [[], [], [], [], [0, 1, 2, 3]]], [[4, 1], [[1, 2, 3], [5, 6, 7, 9, 10, 11], [15, 20, 25], [70, 80, 90, 100], [4, 12, 35]], [[], [], [], [], [0, 1, 2, 3]]], [[5, 1], [[1, 2, 3], [5, 6, 7], [9, 10, 11], [15, 20, 25], [70, 80, 90, 100], [4, 8, 12, 35]], [[], [], [], [], [], [0, 1, 2, 3, 4]]]]
            #operands = [[4, 4, 1, 4], [4, 1, 4, 4], [0, 1, 5, 0], [10, 10, 8, 8]]
            ####
            # no. 2
            # input when leaf and root full
            animTypeList = [0]
            treeList = [[[5, 1], [[1, 2], [4, 5, 6], [8, 10, 15, 20], [40, 50, 60, 700], [100, 200, 420], [3, 7, 30, 80]], [[], [], [], [], [], [0, 1, 2, 3, 4]]]]
            operands = []
            #animTypeList = [1, 1, 1, 1, 0]
            #treeList = [[[5, 1], [[1, 2], [4, 5, 6], [8, 10, 15, 20], [40, 50, 60, 700], [100, 200, 420], [3, 7, 30, 80]], [[], [], [], [], [], [0, 1, 2, 3, 4]]], [[5, 1], [[1, 2], [4, 5, 6], [8, 10, 15, 20], [40, 50, 60, 700], [100, 200, 420], [3, 7, 30, 80]], [[], [], [], [], [], [0, 1, 2, 3, 4]]], [[5, 1], [[1, 2], [4, 5, 6], [8, 10, 17, 20], [40, 50, 60, 700], [100, 200, 420], [3, 7, 30, 80]], [[], [], [], [], [], [0, 1, 2, 3, 4]]], [[5, 1, 1], [[1, 2], [4, 5, 6], [8, 10, 17, 20], [40, 50, 60, 700], [100, 200, 420], [3, 7, 30, 80], []], [[], [], [], [], [], [0, 1, 2, 3, 4], []]], [[6, 2, 1], [[1, 2], [4, 5, 6], [8, 10], [17, 20], [40, 50, 60, 70], [100, 200, 420], [3, 7], [30, 80], [15]], [[], [], [], [], [], [], [0, 1, 2], [3, 4, 5], [6, 7]]]]
            #operands = [[5, 5, 2, 5, 6], [5, 2, 5, 6, 6], [0, 2, 3, 2, 0], [17, 17, 15, 15, 15]]
            ####
            # no. 3
            # input when root full
            #animTypeList = [1, 1, 0]
            #treeList = [[[1], [[1, 2, 3, 4]], [[]]], [[1, 1], [[1, 2, 4, 5], []], [[], [0]]], [[2, 1], [[1, 2], [4, 5], [3]], [[], [], [0, 1]]]]
            #operands = [[0, 0, 1], [0, 1, 1], [4, 0, 0], [5, 3, 3]]
            ###
            # no. 4
            # search
            #animTypeList = [2, 0]
            #treeList = [[[5, 1], [[1, 2], [4, 5, 6], [9, 10, 15, 20], [40, 50, 60, 700], [100, 200, 420], [3, 8, 30, 80]], [[], [], [], [], [], [0, 1, 2, 3, 4]]], [[5, 1], [[1, 2], [4, 5, 6], [9, 10, 15, 20], [40, 50, 60, 700], [100, 200, 420], [3, 8, 30, 80]], [[], [], [], [], [], [0, 1, 2, 3, 4]]]]
            #operands = [5, [5, 1], True]
            # animation = move key with label 10 from root one node to the left down
            animation = ani.Animation(animTypeList, treeList, operands)
            #animation = ani.Animation(0, [[6, 3, 1], [[1, 2], [7, 8, 9], [15], [33, 40], [50, 69, 70], [9999], [4, 12], [41], [75, 76], [20]], [[], [], [], [], [], [], [0, 1, 2], [3, 4], [5], [6, 7, 8]]], [])
            # btree Visualization object (k = 3, key-width = 0.06, ref-width = 0.03, minNodeDistance = 0.1, nodesList[lowest level, ... , root], keysList, animation=moveKey)
            ####
            # no. 1
            #self.GraphNodes = bt.BTreeVisualization(3, 0.2, 0.03, 0.1, animation)
            ####
            # no. 2
            self.GraphNodes = bt.BTreeVisualization(2, 0.2, 0.03, 0.1, animation)
            self.GraphNodes.initializeTK()
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
            self.GraphNodes.runAnimation()
