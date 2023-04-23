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
        self.children = []
        self.leaf = leaf
