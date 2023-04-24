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
#tree with at least 3 keys and max 6 keys in each node!
testTree = BTree(3)

for i in range(10):
    testTree.insertKey(i*3)

testTree.printTree(testTree.rootNode)