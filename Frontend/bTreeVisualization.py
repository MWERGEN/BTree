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
        bTree = graphPackage.Graph(n = 12, directed = True)
        bTree.add_edges([
            (1,0),(2,1),(3,2),(4,3),(5,1),(6,2),(7,6),(8,7),(9,0),(10,0),(11,10)
        ])
        bTree.vs['label'] = ['0','1','2','3','4','5','6','7','8','9','10','11',]
        layout = bTree.layout('reingold_tilford')
        fig, ax = plt.subplots()
        graphPackage.plot(bTree, target=ax, layout=layout)
        plt.show()

        

    def showVersion(self):
        print(graphPackage.__version__)
