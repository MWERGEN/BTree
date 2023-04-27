#   Created for BTree-MTT on 10.04.23
#
#   Creator: Tim Steiner
#
#   Task: Backend class for bTree.
#
#   Editors:
#       1.  Tim Steiner on 10.04.23
#       2.
#
###############################################
#
#   File description:
#       - B-Tree which consists of edges and nodes
#       - inserting, deleting and searching algorithm
#       - balanceing algorithmn
#
from node import Node
class BTree:
    def __init__(self, k):
        self.rootNode = Node(True)
        self.k = k
        self.numOfNodesPerLevel = []
        self.levels = 0
    

    # insert a key into Btree node. there are two cases which can occur:
    # 1. node is full -> split node and insert then 
    # 2. node is not full -> find right place to insert and insert 
    def insertKey(self,key):
        root = self.rootNode
        #case 1
        # node can hold 2 * order keys
        if len(root.keys) == (2 * self.k ) - 1: 
            # new root node
            temp = Node()
            # reference to child which will hold all smaller keys!
            temp.children.insert(0, root) 
            self.rootNode = temp
            # split the full node
            self.splitNode(temp,0) 
            self.insertNotFull(temp,key)
        # case2
        else:
            self.insertNotFull(root,key) #just insert key into node 


    # split child node at index i of parent
    # parent will have middle key of splitNode
    # splitNode will have all keys which are smaller than parents
    # newNode will have all keys which are greater than parents
    def splitNode(self, parent, i):
        k = self.k
        # node at index i will be splitted
        splitNode = parent.children[i] 
        # second node where are all keys which are greater than the parent key will go
        newNode = Node(splitNode.leaf) 
        # add reference to node which holds all greater keys
        parent.children.insert(i + 1, newNode) 
        # fill parent with splitkey -> middle key
        parent.keys.insert(i, splitNode.keys[k - 1]) 
        # take all greater keys and insert them from order to 2 * order - 1
        newNode.keys = splitNode.keys[k: (2 * k) - 1] 
        # take all smaller keys and insert them from 0 to order - 1
        splitNode.keys = splitNode.keys[0: k - 1] 
        if not splitNode.leaf:
            # give newNode with all greater keys all references to all greater children
            newNode.children = splitNode.children[k: 2 * k] 
            # updte references to only smaller children
            splitNode.children = splitNode.children[0: k - 1] 


    # insert key into not full node
    # there are two cases:
    # 1. if node is leaf -> find correct place to insert and insert
    # 2. if node is not a leaf -> find correct node 
    def insertNotFull(self, node, key):
        # size of the keys list
        i = len(node.keys) - 1 
        if node.leaf: 
            # make space for one more key
            node.keys.append(None) 
            # compare every node key to insertion key 
            while i >= 0 and key < node.keys[i]: 
                # shift key one place to the right
                node.keys[i + 1] = node.keys[i] 
                i -= 1
            # insert key to correct place
            node.keys[i + 1] = key 
        else:
            # loop until first key which is smaller 
            while i >= 0 and key < node.keys[i]: 
                i -= 1
            # + 1 because insertion key must come after the first node key which is smaller
            i += 1 
            # check if node where key should go is full -> children[i] means all keys in this node are smaller!
            if len(node.children[i].keys) == (2 * self.k) - 1: 
                # split node to make room for new key 
                self.splitNode(node, i) 
                if key > node.keys[i]:
                    i += 1
            self.insertNotFull(node.children[i], key)



    #TODO implement deleting key
    def deleteKey(key):
        null

    # search key in node
    # go through node and check if key is there
    # if not and node has no children -> key is not in the tree
    # if node has children go to child node with current index i
    def searchKey(self, key, nextNode = None):
        # if function is called recursively
        if nextNode is not None: 
            i = 0
            # go through node and check at which point key is smaller
            while i < len(nextNode.keys) and key > nextNode.keys[i]: 
                i += 1
            if i < len(nextNode.keys) and key == nextNode.keys[i]:
                return nextNode
            # if keys is not found and node is a leaf -> key is not in the tree
            elif nextNode.leaf: 
                return None
            #go to node in which key maybe is 
            return self.searchKey(key, nextNode.children[i]) 
        else:
            # if function is called for the first time it goes from the root 
            self.searchKey(key,self.rootNode) 


    # print tree
    def printTree(self, node, level = 0):
        print("Level ", level, " Anzahl Schlüssel ", len(node.keys))
        for i in node.keys:
            print(i)
        print()
        level += 1
        if len(node.children) > 0:
            for i in node.children:
                self.printTree(i, level)

    # function returns list for frontend which contains numbers of nodes per level
    # 
    def getNumOfNodesPerLevel(self,node,level = 0):
        self.numOfNodesPerLevel.insert(level, self.numOfNodesPerLevel[level] + 1 )
        if not node.leaf:
            level += 1
            for i in node.children:
                self.getNumOfNodesPerLevel(i,level)
    

    # function that counts the numbers of levels the tree has for the list which will be sent to the frontend
    # level 1 -> root
    def getNumOfLevels(self, node, level = 0):
        self.levels += 1
        if not node.leaf:
            self.getNumOfLevels(node.children[0])

    
    # prepares the node list per level
    # for each level it adds one index
    def initNodeList(self):
        for i in range(self.levels):
            self.numOfNodesPerLevel.append(0)

