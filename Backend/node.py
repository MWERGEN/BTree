#   Created for BTree-MTT on 10.04.23
#
#   Creator: Tim Steiner
#
#   Task: Nodes for the B-tree to store keys
#
#   Editors:
#       1.  Tim Steiner on 10.04.23
#       2.
#
###############################################
#
#   File description:
#       - Nodes for the B-tree to store keys
#
class Node:
    def __init__(self, leaf = False):
        self.keys = []
        self.children = [None]
        self.leaf = leaf


    #print node
    def __str__(self):
        return f"{self.keys}"
    
    def __repr__(self):
        return f"{self.keys}"


    def getKeys(self):
        return self.keys
    
    def getNumOfKeys(self):
        return len(self.keys)
    