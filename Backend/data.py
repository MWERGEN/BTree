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

# testing bTree in backend
# tree with at least 3 keys and max 6 keys in each node!
testTree = BTree(2)

for i in range(10):
    testTree.insertKey(i*3)


testTree.printTree(testTree.rootNode)

#get number of levels for the curent tree
testTree.getNumOfLevels(testTree.rootNode)
# initialise list for frontend with the number of levels as indices
testTree.initNodeList()
# create a list for frontend with numbers of nodes per level where 0 is the root
testTree.getNumOfNodesPerLevel(testTree.rootNode)

# frontend needs the list in reveresed order so reverse it
testTree.prepareNodeList()
print(testTree.numOfNodesPerLevel)

# set keys per level from lowest level left to right
testTree.getKeysPerLevel()
print(testTree.keysPerLevel)

# give each node from lowest level left to right ids
# leftest child -> id = 0
testTree.updateNodeIds(testTree.rootNode)