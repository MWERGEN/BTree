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
    def __init__(self, order):
        self.rootNode = Node(True)
        self.order = order


    #insert a key into Btree node. there are two cases which can occur:
    # 1. node is full -> split node and insert then 
    # 2. node is not full -> find right place to insert and insert 
    def insertKey(self,key):
        root = self.rootNode
        #case 1
        if len(root.keys) == (2 * self.order ) - 1: #node can hold 2 * order keys
            temp = Node() #new root node
            temp.children.insert(0, root) #reference to child which will hold all smaller keys!
            self.rootNode = temp
            self.splitNode(temp,0) #split the full node
            self.insertNotFull(temp,key)
        #case2
        else:
            self.insertNotFull(root,key) #just insert key into node 


    #split child node at index i of parent
    #parent will have middle key of splitNode
    #splitNode will have all keys which are smaller than parents
    #newNode will have all keys which are greater than parents
    def splitNode(self, parent, i):
        order = self.order
        splitNode = parent.children[i] #node at index i will be splitted
        newNode = Node(splitNode.leaf) #second node where are all keys which are greater than the parent key will go
        parent.children.insert(i + 1, newNode) #add reference to node which holds all greater keys
        parent.keys.insert(i, splitNode.keys[order - 1]) #fill parent with splitkey -> middle key
        newNode.keys = splitNode.keys[order: (2 * order) - 1] #take all greater keys and insert them from order to 2 * order - 1
        splitNode.keys = splitNode.keys[0: order - 1] #take all smaller keys and insert them from 0 to order - 1
        if not splitNode.leaf:
            newNode.children = splitNode.children[order: 2 * order] #give newNode with all greater keys all references to all greater children
            splitNode.children = splitNode.children[0: order - 1] #updte references to only smaller children


    #insert key into not full node
    #there are two cases:
    #1. if node is leaf -> find correct place to insert and insert
    #2. if node is not a leaf -> find correct node 
    def insertNotFull(self, node, key):
        i = len(node.keys) - 1 #size of the keys list
        if node.leaf: 
            node.keys.append(None) #make space for one more key
            while i >= 0 and key < node.keys[i]: #compare every node key to insertion key 
                node.keys[i + 1] = node.keys[i] #shift key one place to the right
                i -= 1
            node.keys[i + 1] = key #insert key to correct place
        else:
            while i >= 0 and key < node.keys[i]: #loop until first key which is smaller 
                i -= 1
            i += 1 # + 1 because insertion key must come after the first node key which is smaller
            if len(node.children[i].keys) == (2 * self.order) - 1: #check if node where key should go is full -> children[i] means all keys in this node are smaller!
                self.splitNode(node, i) #split node to make room for new key 
                if key > node.keys[i]:
                    i += 1
            self.insertNotFull(node.children[i], key)



    #TODO implement deleting key
    def deleteKey(key):
        null

    #search key in node
    #go through node and check if key is there
    #if not and node has no children -> key is not in the tree
    #if node has children go to child node with current index i
    def searchKey(self, key, nextNode = None):
        if nextNode is not None: #if function is called recursively
            i = 0
            while i < len(nextNode.keys) and key > nextNode.keys[i]: #go through node and check at which point key is smaller
                i += 1
            if i < len(nextNode.keys) and key == nextNode.keys[i]:
                return nextNode
            elif nextNode.leaf: #if keys is not found and node is a leaf -> key is not in the tree
                return None
            return self.searchKey(key, nextNode.children[i]) #go to node in which key maybe is 
        else:
            self.searchKey(key,self.rootNode) #if function is called for the first time it goes from the root 


    #print tree
    def printTree(self, node, l=0):
        print("Level ", l, " Anzahl Schlüssel ", len(node.keys))
        for i in node.keys:
            print(i)
        print()
        l += 1
        if len(node.children) > 0:
            for i in node.children:
                self.printTree(i, l)


