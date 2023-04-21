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
from node import Node

#testing bTree in backend
#array for nodes
nodes = Node(None,None,None) 

#root
rootNode = Node(0,None,nodes)
#tree with root node 0
test = BTree(rootNode,nodes)
print(test) #empty tree

#insert a key
test.insertKey(34)
print(test)

test.insertKey(2)
test.insertKey(69)
test.insertKey(12)
print(test)