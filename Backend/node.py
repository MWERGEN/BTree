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
    def __init__(self):
        self.keys = []
        self.parent = None
        self.child = [None]
        self.leaf = True


    #print node
    def __str__(self):
        return f"{self.keys}"
    
    def __repr__(self):
        return f"{self.keys}"


    def getKeys(self):
        return self.keys
    
    #add key to Node
    def addKey(self, key):
        self.keys.append(key)

    def searchKey(self, key):
        i = 0
        while i < self.n and key >= self.key[i]:
            i += 1
        if i < self.n and key == self.key[i]:
            return self
        if self.leaf:
            return None
        return self.searchKey(self.child[i], key)