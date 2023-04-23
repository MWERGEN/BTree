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
        #root has space for key
        root = self.rootNode
        if root.getNumOfKeys() < 2 * self.order:
            self.rootNode.keys.append(key)
        else:
            #place key in different node
            print('root full')
            #no other nodes
            if len(self.rootNode.children) == 0:
                newNode = Node(True)
                if newNode.addKeyToNode(key, self.order) is None:
                    print('passt')
                    self.rootNode.children.append(newNode) #give ref to new node
            else:
                print('there are different nodes!')
    

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
    def printTree(self,rootNode, level = 0 ):
        print(level ," " , rootNode.keys)
        for child in rootNode.children:
            self.printTree(child, level + 1)


