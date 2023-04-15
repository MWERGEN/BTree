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
#       - visualization of the B-tree
#
import igraph as graphPackage
import matplotlib.pyplot as plt

class BTreeVisualization:
    def drawTree(self):
        bTree = graphPackage.Graph()
        g = graphPackage.Graph(n=4, edges=[[0, 1], [0, 2]])
        layout = g.layout(layout='auto')
        coords_subgraph = layout[:2]  # Coordinates of the first two vertices
        fig, ax = plt.subplots()
        graphPackage.plot(g, target=ax)
        plt.show()

        

    def showVersion(self):
        print(graphPackage.__version__)
