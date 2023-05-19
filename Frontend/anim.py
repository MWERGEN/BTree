#   Created for BTree-MTT on 03.05.23
#
#   Creator: Marius Wergen
#
#   Task: 
#
#   Editors:
#       1.  Marius Wergen on 03.05.23
#       2.  Marius Wergen on 04.05.23
#
###############################################
#
#   File description:
#       - animation class
#

class Animation:
    # constructor
    def __init__(self, type, tree, operands):
        # type of animation
        # type = 0 means 'no animation'
        # type = 1 means 'moving node'
        self.types = type
        self.type = self.types[0]
        self.tree = tree
        # list with how many nodes per level
        # starting on leaf-level
        self.nodesList = tree[0][0]
        # list with all nodes' keys
        # format:
        #   [[key1, key2, ...], [key1, key2, ...], ...] 
        #       first node          sec. node
        self.keysList = tree[0][1]
        # list for edges each connecting two nodes
        self.edgesList = tree[0][2]
        # indicates if animation is finished and can be deleted
        self.finished = False
        # indicates what part of the animation is triggered
        self.walkthrough = 0

        #######################################################
        #   operands initialization depending on animation type
        #######################################################

        # for type = 1 or 2:
        if self.type == 1 or self.type == 2:

            # number which key inside an observed node is looked at
            self.highlightedKey = 0
            # a key > label was found or the last key in observed node is lower than the label
            self.flagOuterKeyReached = False
            # label would be the highest in the observed node
            self.flagNewKeyHighest = False
            # helps scheduling the animation
            self.resetted = False
            
        # for type = 1:
        if self.type == 1:

            ##############
            # moving node
            ##############

            # key moves upwards
            self.upwards = False
            self.operands = operands
            # node where moving node starts
            self.startingNode = operands[0]
            # node where moving node arrives
            self.destinationNode = operands[1]
            # determines on which ref inside the starting node the moving node starts
            self.refInsideStartingNode = operands[2]
            # label inside the moving node
            self.label = operands[3][self.walkthrough]
            # label bold
            self.labelFormatted = ['$\\mathbf{' + str(self.label) + '}$']
            # current x-position of the moveable node
            self.currX = [0]
            # current y-position of the moveable node
            self.currY = [0]
            # x position where the moveable node starts
            self.startingRefX = 0
            # y position where the moveable node starts
            self.startingRefY = 0
            # x position where the moveable node ends after animation
            self.destinationRefX = 0
            # y position where the moveable node ends after animation
            self.destinationRefY = 0
            # gradient for interpolation of the edge connecting the starting node and the ending node
            self.gradient = 0
            # the speed with which the node moves
            # means node-height descends by animationSpeed every frame
            # new x-position will be calculated with the gradient
            self.animationSpeed = 0.02
            # flag for indicating that the node should not move at the moment
            self.flagNoMove = True
            self.newRoot = False

        # for type = 2:
        if self.type == 2:

            ##############
            # search node
            ##############

            self.searchKey = operands[0]
            self.checkNodes = operands[1]
            self.found = operands[2]

    
    def updateNewAnimation(self):
        self.type = self.types[self.walkthrough]
        self.nodesList = self.tree[self.walkthrough][0]
        self.keysList = self.tree[self.walkthrough][1]
        self.edgesList = self.tree[self.walkthrough][2]

    ###########################
    #   functions for type = 1
    ###########################

    # sets label in a bold-formatted manner
    def setLabel(self, label):
        # LaTex expression makes label bold
        self.labelFormatted = ['$\\mathbf{' + str(label) + '}$']