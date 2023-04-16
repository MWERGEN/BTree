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
        bTree = graphPackage.Graph(n = 3, directed = True)
        bTree.add_edges([
            (0,1),(0,2)
        ])
        bTree.vs['label'] = ['0','1','2']
        layout = bTree.layout('tree') #tree layout
        layout.rotate(180) #needs to be rotatet, otherwise it would be upside down
        visual_style = {}
        visual_style['vertex_shape'] = 'rectangle'
        fig, ax = plt.subplots()
        graphPackage.plot(bTree, target=ax, layout=layout,**visual_style)
        plt.show()

        

    def showVersion(self):
        print(graphPackage.__version__)
