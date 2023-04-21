#   Created for BTree-MTT on 10.04.23
#
#   Creator: Tim Steiner
#
#   Task: 
#
#   Editors:
#       1.  Tim Steiner on 10.04.23
#       2.
#
###############################################
#
#   File description:
#       - edges to connect each node of the B-tree
#
class Edge:
    def __init__(self, parent, child):
        self.parent = parent
        self.children = child