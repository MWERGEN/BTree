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


    #TODO implement inserting a key
    def insertKey(self,key):
        root = self.rootNode 
        if len(root.keys) == (2 * self.order ): #if to many keys -> split node
            temp = Node()
            temp.children.insert(0, root) #reference to child
            self.rootNode = temp
            self.splitNode(temp,0) #split the full node
            self.insertNotFull(temp,key)
        #node has space so add key in it
        else:
            self.insertNotFull(root,key)


    #TODO implement split node
    #split child node
    def splitNode(self, parent, i):
        order = self.order
        splitNode = parent.children[i] #node which will be splitted
        newNode = Node(splitNode.leaf) #second node where the other half of the keys will go 
        parent.children.insert(i + 1, newNode) #add reference to children 
        parent.keys.insert(i, splitNode.keys[order - 1]) #fill parent with splitkey
        newNode.keys = splitNode.keys[order: (2 * order) - 1]
        splitNode.keys = splitNode.keys[0: order - 1]
        if not splitNode.leaf:
            newNode.children = splitNode.children[order: 2 * order]
            splitNode.children = splitNode.children[0: order - 1]


    #insert key into not full node
    def insertNotFull(self, node, key):
        i = len(node.keys) - 1 #size of the keys list
        if node.leaf: #if node is leaf just find correct place to insert key
            node.keys.append(None) #make space for one more key
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i] #shift key one place to the right
                i -= 1
            node.keys[i + 1] = key
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == (2 * self.order) - 1:
                self.splitNode(node, i)
                if key > node.keys[i]:
                    i += 1
            self.insertNotFull(node.children[i], key)



    #TODO implement deleting key
    def deleteKey(key):
        null

    #TODO search key
    def searchKey(self,key, nextNode = None):
        null
    

    #TODO balancing algorithmn
    def balanceTree():
        null


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


