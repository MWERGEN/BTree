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
#       - user data from the GUI
#
from bTree import BTree
from edge import Edge
from node import Node

#testing bTree in backend
testNode = Node(1,None)
rootEdges = Edge(None,testNode)
rootNode = Node(0,rootEdges)
test = BTree(rootNode,testNode,rootEdges)
print(test)