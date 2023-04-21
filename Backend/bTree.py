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
        null
    

    #TODO implement deleting key
    def deleteKey(key):
        null

    #TODO search key
    def searchKey(self,key, node = None):
        null

    #TODO balancing algorithmn
    def balanceTree():
        null

    #print bTree to console
    def __str__(self):
        return f"{self.rootNode}"