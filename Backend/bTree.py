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
        rootNode = None
        self.nodes = []
        self.order = order


    #TODO implement inserting a key
    def insertKey(self,key):
        #if tree is empty, make root node and insert key
        if not self.nodes:
            self.rootNode = Node()
            self.rootNode.addKey(key)
            self.nodes.append(self.rootNode)
        #search right node to insert
    

    #TODO implement deleting key
    def deleteKey(key):
        null

    #TODO search key
    def searchNode(self,key):
        null

    #TODO balancing algorithmn
    def balanceTree():
        null

    #print bTree to console
    def __str__(self):
        return f"{self.nodes}"