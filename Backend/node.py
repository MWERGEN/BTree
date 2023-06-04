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
#       - Nodes for the B-tree to store keys
#

class Node:
    def __init__(self, leaf = False):
        self.keys = []
        self.id = 0
        self.children = []
        self.leaf = leaf
