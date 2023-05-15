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
class Backend:
    def __init__(self, k):
        self.btree = BTree(k)
        self.treeNodesPerLevel = None
        self.treeKeysPerLevel = None
        self.sourceDestination = None

    def insertKeyIntoTree(self, key):
        self.treeNodesPerLevel = []
        self.treeKeysPerLevel = []
        self.sourceDestination = []
        self.btree.keysPerLevel = []
        self.btree.nodeIds = []
        # call function which inserts key into tree
        self.btree.insertKey(key)
        # prepare nodes per level list for frontend
        #self.btree.getNumOfNodesPerLevel()
        #print(self.btree.numOfNodesPerLevel)
        self.treeNodesPerLevel = self.btree.numOfNodesPerLevel
        # prepare keys per level for frontend
        self.btree.getKeysPerLevel()
        self.treeKeysPerLevel = self.btree.keysPerLevel
        # set source destination for key insertion
        self.sourceDestination = self.btree.visitiedNodes
        # set the numbers of nodes per level
        # at index 0 is leftest leaf
        levels = self.btree.countNodesPerLevel()
        self.btree.numOfNodesPerLevel = levels.copy()
        self.treeNodesPerLevel = levels



testData = Backend(2)
testData.insertKeyIntoTree(3)
testData.insertKeyIntoTree(4)
testData.insertKeyIntoTree(5)
testData.insertKeyIntoTree(1)
testData.insertKeyIntoTree(2)
testData.insertKeyIntoTree(7)
testData.insertKeyIntoTree(99)
testData.insertKeyIntoTree(12)
testData.insertKeyIntoTree(18)
testData.insertKeyIntoTree(24)
print(testData)
