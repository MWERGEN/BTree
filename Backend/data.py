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
#tree with at least 1 keys and max 2 keys in each node!
testTree = BTree(3)

#insert one key
testTree.insertKey(7)
testTree.insertKey(1)
testTree.insertKey(8)
testTree.insertKey(12)

testTree.insertKey(10)
testTree.insertKey(16)
testTree.insertKey(2)


testTree.printTree(testTree.rootNode)