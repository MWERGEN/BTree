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
    def __init__(self, key,edges):
        self.key = key
        self.edges = edges


    #print node
    def __str__(self):
        return f"{self.key}"