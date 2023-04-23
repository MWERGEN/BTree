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

#testing bTree in backend
#tree with at least 2 keys and max 4 keys in each node!
testTree = BTree(1)

#insert one key
testTree.insertKey(2)
testTree.insertKey(3)
testTree.insertKey(10)
testTree.insertKey(54)

testTree.printTree(testTree.rootNode)