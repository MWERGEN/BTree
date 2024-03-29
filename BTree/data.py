#   Created for BTree-MTT on 10.04.23
#
#   Creator: Tim Steiner
#
#   Editors:
#       1.  Tim Steiner on 10.04.23
#
###############################################
#
#   File description:
#       - user data from the GUI
#

# local imports
from Backend import bTree

class Backend:
    def __init__(self, k):
        self.btree = bTree.BTree(k)
        self.treeNodesPerLevel = None
        self.treeKeysPerLevel = None
        self.sourceDestination = None
        self.animationList = []
        self.references = []
        self.usedKeys =[]
        self.treeList = []
        self.operands = []
        self.searchedNodes = []

    def insertKeyIntoTree(self, key):
        # reset all parameters of backend object
        self.treeNodesPerLevel = []
        self.treeKeysPerLevel = []
        self.sourceDestination = []
        self.btree.keysPerLevel = []
        self.btree.nodeIds = []
        self.btree.animationList = []
        self.edgeLists = []
        self.treeNodesPerLevel = []
        self.references = []
        self.treeList = []
        self.operands = []
        # call function which inserts key into tree
        self.btree.insertKey(key)
        # prepare nodes per level list for frontend
        self.treeNodesPerLevel = self.btree.numOfNodesPerLevel
        # prepare keys per level for frontend
        #self.btree.getKeysPerLevel()
        self.treeKeysPerLevel = self.btree.keysPerLevelCopies
        # set source destination for key insertion
        self.sourceDestination = self.btree.visitiedNodes
        # set the numbers of nodes per level
        # at index 0 is leftest leaf
        #levels = self.btree.countNodesPerLevel()
        #self.btree.numOfNodesPerLevel = levels.copy()
        self.treeNodesPerLevel = self.btree.numOfNodesPerLevelCopies
        # set animation list
        self.animationList = self.btree.animationList
        self.edgeLists = self.btree.edgeListCopies
        # set references 
        self.references = self.btree.usedReferences
        #set used keys
        self.usedKeys = self.btree.usedKeys
        # temp var for iterations for treelisr
        iterations = len(self.animationList)
        # big tree list for frontend which contains of 1. num of nodes per level 2. keys per level 3. edgelist
        for i in range(iterations):
            temp = []
            temp.append(self.treeNodesPerLevel[i])
            temp.append(self.treeKeysPerLevel[i])
            temp.append(self.edgeLists[i])
            self.treeList.append(temp)
        self.operands = self.sourceDestination
        self.operands.append(self.references)
        self.operands.append(self.usedKeys)


    def searchKeyInTree(self, key):
        # reset all parameters of backend object
        self.treeNodesPerLevel = []
        self.treeKeysPerLevel = []
        self.sourceDestination = []
        self.btree.keysPerLevel = []
        self.btree.nodeIds = []
        self.animationList = []
        self.btree.animationList = []
        self.btree.searchedNodes = []
        self.edgeLists = []
        self.treeNodesPerLevel = []
        self.references = []
        self.treeList = []
        self.operands = []
        self.searchedNodes = []
        # var to check if key is found
        keyFound = False
        self.animationList.append(2)
        self.animationList.append(0)
        # call function which searchs key
        if not self.btree.searchKey(key,self.btree.rootNode) == None:
            keyFound = True
        self.searchedNodes = self.btree.searchedNodes
        self.operands.append(key)
        self.operands.append(self.searchedNodes)
        self.operands.append(keyFound)
        # search needs two tree lists so the animations works right
        temp = []
        list = self.btree.getTreeListForSearch()
        temp.append(list[0])
        temp.append(list[0])
        self.treeList = temp
        print('test')

    def deleteKeyFromTree(self, key):
        # reset all parameters of backend object
        self.treeNodesPerLevel = []
        self.treeKeysPerLevel = []
        self.sourceDestination = []
        self.btree.keysPerLevel = []
        self.btree.nodeIds = []
        self.animationList = []
        self.btree.animationList = []
        self.btree.searchedNodes = []
        self.edgeLists = []
        self.treeNodesPerLevel = []
        self.references = []
        self.treeList = []
        self.operands = []
        self.searchedNodes = []
        # key in tree?
        keyFound = False
        self.animationList.append(2)
        self.animationList.append(0)
        if self.btree.searchKey(key, self.btree.rootNode):
            keyFound = True
            deleted = self.btree.deleteKey(key, self.btree.rootNode)
            self.searchedNodes = self.btree.searchedNodes
            self.treeNodesPerLevel = self.btree.numOfNodesPerLevelCopies
            self.treeKeysPerLevel = self.btree.keysPerLevelCopies
            self.edgeLists = self.btree.edgeListCopies
            # temp var for iterations for treelist
            iterations = len(self.animationList)
            for i in range(iterations):
                temp = []
                temp.append(self.treeNodesPerLevel[i])
                temp.append(self.treeKeysPerLevel[i])
                temp.append(self.edgeLists[i])
                self.treeList.append(temp)
            self.operands.append(key)
            self.operands.append(self.searchedNodes)
            self.operands.append(deleted)
            print('test')
        else:
            # search needs two tree lists so the animations works right
            self.searchedNodes = self.btree.searchedNodes
            temp = []
            list = self.btree.getTreeListForSearch()
            temp.append(list[0])
            temp.append(list[0])
            self.treeList = temp
            self.operands.append(key)
            self.operands.append(self.searchedNodes)
            self.operands.append(keyFound)
    
    def resetTree(self):
        # reset all parameters of backend object
        self.treeNodesPerLevel = []
        self.treeKeysPerLevel = []
        self.sourceDestination = []
        self.btree.keysPerLevel = []
        self.btree.nodeIds = []
        self.animationList = []
        self.btree.animationList = []
        self.btree.searchedNodes = []
        self.edgeLists = []
        self.treeNodesPerLevel = []
        self.references = []
        self.treeList = []
        self.operands = []
        self.searchedNodes = []
        # animation list for reset is just 0
        self.animationList.append(0)
        temp = self.btree.reset()
        self.treeList.append(temp)


    def changeK(self,k):
        # delete old tree and create new one with new k
        self.btree = None
        self.btree = bTree.BTree(k)
        # make sure everything is changed
        self.resetTree()
