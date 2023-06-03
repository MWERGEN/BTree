#   Created for BTree-MTT on 10.04.23
#
#   Creator: Tim Steiner
#
#   Task: Backend class for bTree.
#
#   Editors:
#       1.  Tim Steiner on 10.04.23
#       2.
#
###############################################
#
#   File description:
#       - B-Tree which consists of edges and nodes
#       - inserting, deleting and searching algorithm
#       - preparing lists for frontend (num of nodes per level, keys per level and edges)
#
# when executed by main
from Backend import node
# debugging
#import node
from collections import deque

class BTree:
    def __init__(self, k):
        self.rootNode = node.Node(True)
        # num of keys is min k and max 2 * k
        self.k = k
        # how many nodes per level starting from the bottom -> last item always 1 means root
        self.numOfNodesPerLevel = []
        # for every animation step frontend needs the number of nodes per level
        self.numOfNodesPerLevelCopies = []
        # depth of btree 0 is root level 
        self.levels = 0
        # keys per level in reversed level order from left to right
        self.keysPerLevel = []
        # list of keys per level for each step of animations
        # list contains keysPerLevel lists
        self.keysPerLevelCopies = []
        # ids from each node in reversed level order from left to right
        self.nodeIds = []
        # all edges represented with node id first item is from second is to
        self.edgeList = []
        # list of edge lists for each step of animations
        self.edgeListCopies = []
        # what kind of animations should be displayed
        self.animationList = []
        # holds the nodes which are visited while the animation first list is source second list is target 
        self.visitiedNodes = []
        # list of uses references 
        self.usedReferences = []
        # list of used keys for animation
        self.usedKeys = []
        # list for searching algorithmn, contains all searched node ids
        self.searchedNodes = []
        self.fullRoot = False
        self.intoRoot = False



    # insert a key into Btree node. there are two cases which can occur:
    # 1. node is full -> split node and insert then 
    # 2. node is not full -> find right place to insert and insert 
    def insertKey(self,key):
        test = False
        root = self.rootNode
        # give root id 0
        self.updateNodeIds(self.rootNode)
        # new key -> new animation
        self.animationList = []
        self.visitiedNodes = []
        # for every step of the animation frontend needs the keys per level
        self.keysPerLevelCopies = []
        self.keysPerLevel = []
        # for every step of the animation frontend needs edge list
        self.edgeList = []
        self.edgeListCopies = []
        # for every step of the animation frontend needs num of nodes per level
        self.numOfNodesPerLevel = []
        self.numOfNodesPerLevelCopies = []
        # temp lists to fill visited nodes will be filled while inserting 
        source = []
        target = []
        # reset used references
        self.usedReferences = []
        # reset used keys
        self.usedKeys = []
        # first step of every insertion animation is from root to root
        source.append(self.rootNode.id)
        target.append(self.rootNode.id)
        self.visitiedNodes.append(source)
        self.visitiedNodes.append(target)
        # set keys per level list -> has to be copy of list because every key list can be different!
        self.getKeysPerLevel()
        keysPerLevelBeforeInsert = self.keysPerLevel[:]
        self.keysPerLevelCopies.append([list(l) for l in keysPerLevelBeforeInsert])
        # edge list copy
        self.setEdgeList(self.rootNode)
        edgeListBeforeInsert = self.edgeList[:]
        self.edgeListCopies.append([list(l) for l in edgeListBeforeInsert])
        # num of nodes list copy
        nodePerLevelBefore = self.countNodesPerLevel()
        self.numOfNodesPerLevelCopies.append(nodePerLevelBefore)
        # used key is inserted key
        self.usedKeys.append(key)
        # every animation starts with a zero reference
        self.usedReferences.append(0)
        #case 1
        # node can hold 2 * order keys
        if len(root.keys) == 2 * self.k:
            # check if root has children
            if not root.children: 
                # new root node
                temp = node.Node()
                 # edge list copy
                self.setEdgeList(self.rootNode)
                edgeListBeforeInsert = self.edgeList[:]
                self.edgeListCopies.append([list(l) for l in edgeListBeforeInsert])
                # reference to child which will hold all smaller keys!
                temp.children.insert(0, root) 
                self.rootNode = temp
                # get the current keys per level of the tree
                nodePerLevelBefore = self.countNodesPerLevel()
                self.numOfNodesPerLevelCopies.append(nodePerLevelBefore)
                # set keys per level list -> has to be copy of list because every key list can be different!
                self.getKeysPerLevel()
                keysPerLevelBeforeSplit = self.keysPerLevel[:]
                self.keysPerLevelCopies.append([list(l) for l in keysPerLevelBeforeSplit])
                # split the full node
                self.splitNode(temp, key,0,False) 
                #self.insertNotFull(temp,key, source, target)
                # key is inserted so animation is over -> 0
                self.animationList.append(0)
                # there is a new node in the tree so update the ids of the nodes
                # this ensures that at every operation the node ids are correct
                self.updateNodeIds(self.rootNode)
                source.append(0)
                target.append(0)
                # keys per level copies
                self.getKeysPerLevel()
                self.keysPerLevelCopies.append(self.keysPerLevel.copy())
                # edge list copy
                self.setEdgeList(self.rootNode)
                edgeListBeforeSplit = self.edgeList[:]
                self.edgeListCopies.append([list(l) for l in edgeListBeforeSplit])
            else:
                # root has children where key can be inserted
                i = len(root.keys) - 1
                # loop until first key which is smaller 
                while i >= 0 and key < root.keys[i]: 
                    i -= 1
                # + 1 because insertion key must come after the first node key which is smaller
                i += 1
                self.animationList.append(1)
                self.usedReferences.append(i)
                self.usedKeys.append(key)
                self.visitiedNodes[0].append(root.id)
                self.visitiedNodes[1].append(root.children[i].id)
                # check if node where key should go is full -> children[i] means all keys in this node are smaller!
                if root.children[i].leaf and len(root.children[i].keys) == (2 * self.k):
                    # get the current keys per level of the tree
                    nodePerLevelBeforeFullRootSplit = self.countNodesPerLevel()
                    self.numOfNodesPerLevelCopies.append(nodePerLevelBeforeFullRootSplit)
                    # set keys per level list -> has to be copy of list because every key list can be different!
                    self.getKeysPerLevel()
                    keysPerLevelBeforeFullRootSplit = self.keysPerLevel[:]
                    self.keysPerLevelCopies.append([list(l) for l in keysPerLevelBeforeFullRootSplit])
                    # edge list copy
                    self.setEdgeList(self.rootNode)
                    edgeListBeforeRootSplit = self.edgeList[:]
                    self.edgeListCopies.append([list(l) for l in edgeListBeforeRootSplit])
                    # reset target where node will be split
                    targetNode = i
                    sourceNode = self.rootNode.id
                    self.visitiedNodes[0].append(sourceNode)
                    self.visitiedNodes[1].append(targetNode)
                    # split node to make room for new key 
                    self.splitNode(root, key,i,True) 
                    test = True
                    #if key > root.keys[i]:
                    #   i += 1
                if not test:
                    # set keys per level list -> has to be copy of list because every key list can be different!
                    self.getKeysPerLevel()
                    keysPerLevelBeforeInsertFullRoot = self.keysPerLevel[:]
                    self.keysPerLevelCopies.append([list(l) for l in keysPerLevelBeforeInsertFullRoot])
                    # edge list copy
                    self.setEdgeList(self.rootNode)
                    edgeListBeforeInsertFullRoot = self.edgeList[:]
                    self.edgeListCopies.append([list(l) for l in edgeListBeforeInsertFullRoot])
                    # num of nodes list copy
                    nodePerLevelBeforeFullRoot = self.countNodesPerLevel()
                    self.numOfNodesPerLevelCopies.append(nodePerLevelBeforeFullRoot)
                    self.insertNotFull(root.children[i], key, source, target, False,False)
                    # key is inserted so animation is over -> 0
                    self.animationList.append(0)
                    # root is no longer full
                    self.fullRoot = False
        # case2
        else:
            # just insert key into node 
            self.insertNotFull(root,key, source, target,False,False) 
            # key is inserted so animation is over -> 0
            self.animationList.append(0)
            


    # split child node at index i of parent
    # parent will have middle key of splitNode
    # splitNode will have all keys which are smaller than parents
    # newNode will have all keys which are greater than parents
    def splitNode(self, parent, key, index, fromFullRoot):
        # checks if parent needs to be split
        rootSplit = False
        #source = []
        #target = []
        k = self.k
        self.splitIndex = index
        self.updateNodeIds(self.rootNode)
        source = parent.children[index].id
        target = parent.id 
        fullParent = False
        #self.visitiedNodes[0].append(source)
        #self.visitiedNodes[1].append(target)
        # full node
        splitNode = parent.children[index]
        # second node where are all keys which are greater than the middle key will go
        newNode = node.Node(splitNode.leaf) 
        i = len(splitNode.keys) - 1
        # make space for one more key
        splitNode.keys.append(None) 
        # compare every node key to insertion key 
        while i >= 0 and key < splitNode.keys[i]: 
        # shift key one place to the right
            splitNode.keys[i + 1] = splitNode.keys[i] 
            i -= 1
        # insert key to correct place
        splitNode.keys[i + 1] = key
        self.usedReferences.append(i+1)
        self.animationList.append(1)
        middleIndex = int(len(splitNode.keys) / 2)
        # used key is inserted key
        self.usedKeys.append(splitNode.keys[middleIndex])
        copyOfSplitKey = splitNode.keys[middleIndex]
        del splitNode.keys[middleIndex]
        if parent.keys: 
            # set keys per level list -> has to be copy of list because every key list can be different!
            self.getKeysPerLevel()
            keysPerLevelBeforeSplit = self.keysPerLevel[:]
            self.keysPerLevelCopies.append([list(l) for l in keysPerLevelBeforeSplit])
        # fill parent with splitkey -> middle key
        self.insertNotFull(parent,copyOfSplitKey, source, target, True,False)
        if len(parent.keys) == 2 * k + 1 and len(self.rootNode.keys) == 2 * k:
            fromFullRoot = True
        if not fromFullRoot:
            self.visitiedNodes[0].append(target)
            self.visitiedNodes[1].append(target)
        if not splitNode.leaf:
            # give newNode with all greater keys all references to all greater children
            newNode.children = splitNode.children[k: 2 * k] 
            # updte references to only smaller children
            splitNode.children = splitNode.children[0: k - 1]
        if len(parent.keys) == (2 * self.k ) + 1:
            # root is full -> new root
            if parent is self.rootNode:
                rootSplit = True
                # new root node
                temp = node.Node()
                # reference to child which will hold all smaller keys!
                temp.children.insert(0, parent) 
                self.rootNode = temp
                # give root id 0
                self.updateNodeIds(self.rootNode)
                source = parent.id
                target = self.rootNode.id
                self.visitiedNodes[0].append(source)
                self.visitiedNodes[1].append(target)
                # edge list copy
                self.setEdgeList(self.rootNode)
                edgeListBeforeSplit = self.edgeList[:]
                if edgeListBeforeSplit:
                    root = edgeListBeforeSplit[-1]
                    if root:
                        edge = edgeListBeforeSplit[-1]
                        root.pop()
                self.edgeListCopies.append([list(l) for l in edgeListBeforeSplit])
                edgeListBeforeSplit[-1].append(edge)
                # get the current keys per level of the tree
                nodePerLevelBeforeFullRootSplit = self.countNodesPerLevel()
                self.numOfNodesPerLevelCopies.append(nodePerLevelBeforeFullRootSplit)
                # set keys per level list -> has to be copy of list because every key list can be different!
                self.getKeysPerLevel()
                keysPerLevelBeforeFullRootSplit = self.keysPerLevel[:]
                for lists in keysPerLevelBeforeFullRootSplit:
                    if copyOfSplitKey in lists:
                        listIndex = keysPerLevelBeforeFullRootSplit.index(lists)
                        valueIndex = lists.index(copyOfSplitKey)
                        lists.remove(copyOfSplitKey)
                self.keysPerLevelCopies.append([list(l) for l in keysPerLevelBeforeFullRootSplit])
                keysPerLevelBeforeFullRootSplit[listIndex].insert(valueIndex,copyOfSplitKey)
                # split the full node
                self.splitRoot(temp,0,splitNode) 
                #self.insertNotFull(temp,key, source, target)
                # key is inserted so animation is over -> 0
                self.animationList.append(0)
                source = self.rootNode.id
                target = self.rootNode.id
                self.visitiedNodes[0].append(source)
                self.visitiedNodes[1].append(target)
                # there is a new node in the tree so update the ids of the nodes
                # this ensures that at every operation the node ids are correct
                self.updateNodeIds(self.rootNode)
            # parent is full
            else:
                rootOfParent = self.getParent(parent, self.rootNode)
                fullParent = True
                rootSplit = True
                loopIndex = 0
                indexOfSplit = 0
                for i in rootOfParent.children:
                    loopIndex += 1
                    if i == parent:
                        indexOfSplit = loopIndex
                indexOfSplit -= 1
                self.splitRoot(rootOfParent,indexOfSplit, splitNode)
                print('test')
        if rootSplit:
            parentOfRootSplit = self.getParent(splitNode, self.rootNode)
            # get index of split node
            if parentOfRootSplit is None:
                indexOfOrgSplitNode = self.splitIndex
            else:
                indexOfOrgSplitNode = parentOfRootSplit.children.index(splitNode)
            # take all greater keys and insert them from order to 2 * order - 1
            newNode.keys = splitNode.keys[middleIndex: 2 * k] 
            # take all smaller keys and insert them from 0 to order - 1
            splitNode.keys = splitNode.keys[0: middleIndex]
            # get neighbour
            tempParent = self.getParent(parentOfRootSplit,self.rootNode)
            neighbour = self.getNodeWithId(self.rootNode,parentOfRootSplit.id + 1)
            # check if really neighbour
            if neighbour in tempParent.children and indexOfOrgSplitNode == self.k:
                neighbour.children.insert(0,newNode)
            else:
                parentOfRootSplit.children.insert(indexOfOrgSplitNode + 1, newNode)
            self.updateNodeIds(self.rootNode)
            nodePerLevelAfterRootSplit = self.countNodesPerLevel()
            self.numOfNodesPerLevelCopies.append(nodePerLevelAfterRootSplit)
            # set keys per level list -> has to be copy of list because every key list can be different!
            if not self.fullRoot:
                self.getKeysPerLevel()
                keysPerLevelAfterRootSplit = self.keysPerLevel[:]
                self.keysPerLevelCopies.append([list(l) for l in keysPerLevelAfterRootSplit])
            else:
                self.keysPerLevelCopies.append(self.keysPerLevelCopies[-1])
            # edge list copy
            self.setEdgeList(self.rootNode)
            edgeListAfterRootSplit = self.edgeList[:]
            self.edgeListCopies.append([list(l) for l in edgeListAfterRootSplit])
        if not rootSplit:
            # find correct parent 
            if fullParent:
                print('test')
            # add reference to node which holds all greater keys
            parent.children.insert(index + 1, newNode)
            # take all greater keys and insert them from order to 2 * order - 1
            newNode.keys = splitNode.keys[middleIndex: 2 * k] 
            # take all smaller keys and insert them from 0 to order - 1
            splitNode.keys = splitNode.keys[0: middleIndex]
            self.updateNodeIds(self.rootNode)
            # get the current keys per level of the tree
            nodePerLevelBefore = self.countNodesPerLevel()
            self.numOfNodesPerLevelCopies.append(nodePerLevelBefore)
            self.setEdgeList(self.rootNode)
            edgeListBeforeSplit = self.edgeList[:]
            self.edgeListCopies.append([list(l) for l in edgeListBeforeSplit]) 


    def splitRoot(self, parent, index, willBeSplitt):
        source = parent.id
        target = parent.id
        k = self.k
        fullRoot = False
        # full node
        splitNode = parent.children[index]
        if not parent.keys and parent == self.rootNode:
            if not willBeSplitt in splitNode.children:
                indexOfOrgSplitNode = self.splitIndex
            else:
                indexOfOrgSplitNode = splitNode.children.index(willBeSplitt)
            fullRoot = True
        else:
            indexOfOrgSplitNode = splitNode.children.index(willBeSplitt)
        i = len(splitNode.keys) - 1
        middleIndex = int(len(splitNode.keys) / 2)
        # fill parent with splitkey -> middle key
        self.insertNotFull(parent,splitNode.keys[middleIndex], source, target, True, True)
        # second node where are all keys which are greater than the middle key will go
        newNode = node.Node(splitNode.leaf)
        # add reference to node which holds all greater keys
        parent.children.insert(index + 1, newNode) 
        del splitNode.keys[middleIndex]
        # take all greater keys and insert them from order to 2 * order - 1
        newNode.keys = splitNode.keys[middleIndex: 2 * k] 
        # take all smaller keys and insert them from 0 to order - 1
        splitNode.keys = splitNode.keys[0: middleIndex]
        if fullRoot:
            if indexOfOrgSplitNode < self.k:
                # give newNode with all greater keys all references to all greater children
                newNode.children = splitNode.children[k : 2 * k + 2] 
                # updte references to only smaller children
                splitNode.children = splitNode.children[0: k]
                print('test')
            else:
                # give newNode with all greater keys all references to all greater children
                newNode.children = splitNode.children[k + 1: 2 * k + 2] 
                # updte references to only smaller children
                splitNode.children = splitNode.children[0: k + 1]
            print('test')
        else:
            if indexOfOrgSplitNode < self.k:
                # give newNode with all greater keys all references to all greater children
                newNode.children = splitNode.children[k : 2 * k + 1] 
                # updte references to only smaller children
                splitNode.children = splitNode.children[0: k]
            else:
                # give newNode with all greater keys all references to all greater children
                newNode.children = splitNode.children[k + 1: 2 * k + 1] 
                # updte references to only smaller children
                splitNode.children = splitNode.children[0: k + 1]
                print('test')
            # parent is also full
            if len(parent.keys) == 2 * self.k + 1:
                if parent == self.rootNode:
                    rootSplit = True
                    # split the full node
                    self.fullRoot = True
                    # new root node
                    temp = node.Node()
                    # reference to child which will hold all smaller keys!
                    temp.children.insert(0, parent) 
                    self.rootNode = temp
                    # give root id 0
                    self.updateNodeIds(self.rootNode)
                    source = parent.id
                    target = self.rootNode.id
                    self.visitiedNodes[0].append(source)
                    self.visitiedNodes[1].append(target)
                    middleIndex = int(len(parent.keys) / 2)
                    copyOfSplitKey = parent.keys[middleIndex]
                    # edge list copy
                    self.setEdgeList(self.rootNode)
                    edgeListBeforeSplit = self.edgeList[:]
                    if edgeListBeforeSplit:
                        root = edgeListBeforeSplit[-1]
                        if root:
                            edge = edgeListBeforeSplit[-1]
                            root.pop()
                    self.edgeListCopies.append([list(l) for l in edgeListBeforeSplit])
                    edgeListBeforeSplit[-1].append(edge)
                    # get the current keys per level of the tree
                    nodePerLevelBeforeFullRootSplit = self.countNodesPerLevel()
                    self.numOfNodesPerLevelCopies.append(nodePerLevelBeforeFullRootSplit)
                    # set keys per level list -> has to be copy of list because every key list can be different!
                    self.getKeysPerLevel()
                    keysPerLevelBeforeFullRootSplit = self.keysPerLevel[:]
                    for lists in keysPerLevelBeforeFullRootSplit:
                        if copyOfSplitKey in lists:
                            listIndex = keysPerLevelBeforeFullRootSplit.index(lists)
                            valueIndex = lists.index(copyOfSplitKey)
                            lists.remove(copyOfSplitKey)
                    self.keysPerLevelCopies.append([list(l) for l in keysPerLevelBeforeFullRootSplit])
                    keysPerLevelBeforeFullRootSplit[listIndex].insert(valueIndex,copyOfSplitKey)
                    self.splitRoot(temp,0,parent) 
                    self.updateNodeIds(self.rootNode)
                    #self.insertNotFull(temp,key, source, target)
                    source = self.rootNode.id
                    target = self.rootNode.id
                    self.visitiedNodes[0].append(source)
                    self.visitiedNodes[1].append(target)
                    # there is a new node in the tree so update the ids of the nodes
                    # this ensures that at every operation the node ids are correct
                    self.updateNodeIds(self.rootNode)
                else:
                    source = parent.id
                    target = self.rootNode.id
                    k = self.k
                    fullRoot = False
                    # full node
                    splitNode = parent
                    splitIndex = self.rootNode.children.index(splitNode)
                    i = len(splitNode.keys) - 1
                    middleIndex = int(len(splitNode.keys) / 2)
                    # fill parent with splitkey -> middle key
                    self.intoRoot = True
                    self.insertNotFull(self.rootNode,splitNode.keys[middleIndex], source, target, True, True)
                    # second node where are all keys which are greater than the middle key will go
                    newNode = node.Node(splitNode.leaf)
                    # add reference to node which holds all greater keys
                    self.rootNode.children.insert(splitIndex + 1, newNode)
                    del splitNode.keys[middleIndex]
                    # take all greater keys and insert them from order to 2 * order - 1
                    newNode.keys = splitNode.keys[middleIndex: 2 * k] 
                    # take all smaller keys and insert them from 0 to order - 1
                    splitNode.keys = splitNode.keys[0: middleIndex]
                    newNode.children = splitNode.children[k + 1: 2 * k + 2]
                    splitNode.children = splitNode.children[0: k + 1]
                    self.intoRoot = False
                    print('test')


    def getParent(self, searchNode, rootNode):
        if searchNode in rootNode.children:
            return rootNode
        if len(rootNode.children) > 0:
            for i in rootNode.children:
                parent = self.getParent(searchNode,i)
                if parent is not None:
                    return parent
        else:
            return None
        


    # insert key into not full node
    # there are two cases:
    # 1. if node is leaf -> find correct place to insert and insert
    # 2. if node is not a leaf -> find correct node 
    def insertNotFull(self, node, key, source, target, fromSplit, fromRootSplit):
            test = False
            emptyNode = False
            if len(node.keys) == 0:
                i = 0
                emptyNode = True
            else:
                i = len(node.keys) - 1 
            if node.leaf or fromSplit:
                if emptyNode and not self.fullRoot:
                    node.keys.append(key)
                    self.animationList.append(1)
                    self.usedKeys.append(key)
                    self.usedReferences.append(0)
                    if not fromRootSplit and not fromSplit:
                        # get the current keys per level of the tree
                        nodePerLevelBefore = self.countNodesPerLevel()
                        self.numOfNodesPerLevelCopies.append(nodePerLevelBefore)
                    if not fromSplit:
                        # edge list copy
                        self.setEdgeList(self.rootNode)
                        edgeListBeforeInsert = self.edgeList[:]
                        self.edgeListCopies.append([list(l) for l in edgeListBeforeInsert])
                        # get the current keys per level of the tree
                        self.getKeysPerLevel()
                        keysPerLevelBeforeInsert = self.keysPerLevel[:]
                        self.keysPerLevelCopies.append([list(l) for l in keysPerLevelBeforeInsert])
                        self.visitiedNodes[0].append(0)
                        self.visitiedNodes[1].append(0)
                else:
                    # make space for one more key
                    node.keys.append(None)
                    if i == 0 and node.keys[0] == None:
                        node.keys[0] = key
                        self.usedKeys.append(key)
                    else:
                        # compare every node key to insertion key 
                        while i >= 0 and key < node.keys[i]: 
                            # shift key one place to the right
                            node.keys[i + 1] = node.keys[i] 
                            i -= 1
                        # insert key to correct place
                        node.keys[i + 1] = key
                        self.usedReferences.append(i + 1)
                        if fromSplit:
                            self.visitiedNodes[0].append(source)
                            self.visitiedNodes[1].append(target)
                        else:
                            currentPos = source[-1]
                            source.append(node.id)
                            target.append(node.id)
                    if not self.intoRoot:
                        # animation for comparing 
                        self.animationList.append(1)
                    if not fromSplit:
                        # get the current keys per level of the tree
                        self.getKeysPerLevel()
                        keysPerLevelBeforeInsert = self.keysPerLevel[:]
                        self.keysPerLevelCopies.append([list(l) for l in keysPerLevelBeforeInsert])
                    if not self.fullRoot:
                        # there is a new node in the tree so update the ids of the nodes
                        # this ensures that at every operation the node ids are correct
                        self.updateNodeIds(self.rootNode)
                        if not self.fullRoot:
                            # get current nodes per level
                            nodePerLevelBefore = self.countNodesPerLevel()
                            self.numOfNodesPerLevelCopies.append(nodePerLevelBefore)
                        else:
                            self.numOfNodesPerLevelCopies.append(self.numOfNodesPerLevelCopies[-1])
                        # edge list copy
                        self.setEdgeList(self.rootNode)
                        edgeListBeforeInsert = self.edgeList[:]
                        self.edgeListCopies.append([list(l) for l in edgeListBeforeInsert])
                        # used keys update
                        self.usedKeys.append(key)
            else:
                # animation for traversing + comparing
                self.animationList.append(1)
                # get the current keys per level of the tree
                self.getKeysPerLevel()
                keysPerLevelBeforeInsert = self.keysPerLevel[:]
                self.keysPerLevelCopies.append([list(l) for l in keysPerLevelBeforeInsert])
                # get current nodes per level
                nodePerLevelBefore = self.countNodesPerLevel()
                self.numOfNodesPerLevelCopies.append(nodePerLevelBefore)
                # edge list copy
                self.setEdgeList(self.rootNode)
                edgeListBeforeInsert = self.edgeList[:]
                self.edgeListCopies.append([list(l) for l in edgeListBeforeInsert])
                # used keys update
                self.usedKeys.append(key)
                if not node.keys:
                    node.keys.append(key)
                else:
                    # loop until first key which is smaller 
                    while i >= 0 and key < node.keys[i]: 
                        i -= 1
                    # + 1 because insertion key must come after the first node key which is smaller
                    i += 1
                    if len(node.children) - 1 < i:
                        i -= 1
                    self.usedReferences.append(i)
                    targetNode = node.children[i].id
                    tempSource = node.id
                    self.visitiedNodes[0].append(tempSource)
                    self.visitiedNodes[1].append(targetNode)
                    # check if node where key should go is full -> children[i] means all keys in this node are smaller!
                    if not node.children[i].children:
                        if len(node.children[i].keys) == (2 * self.k):
                            # split node to make room for new key 
                            self.splitNode(node, key,i,False) 
                            test = True
                            # get the current keys per level of the tree
                            self.getKeysPerLevel()
                            keysPerLevelBeforeInsert = self.keysPerLevel[:]
                            self.keysPerLevelCopies.append([list(l) for l in keysPerLevelBeforeInsert])
                            #if key > node.keys[i]:
                             #   i += 1
                    if not test:
                        self.insertNotFull(node.children[i], key, source, target, False,False)


    # delete key inside tree
    # different events can occour
    # if there are enough keys inside the node (k + 1) just delete
    # if not try to get keys from left or right neighbour
    # if they don't have enough merge them
    def deleteKey(self,key, nextNode = None):
        # reset all attributes
        self.numOfNodesPerLevel = []
        self.numOfNodesPerLevelCopies = []
        self.keysPerLevel = []
        self.keysPerLevelCopies = []
        self.edgeList = []
        self.edgeListCopies = []
        self.searchedNodes = []
        deleted = False
        # set keys per level list -> has to be copy of list because every key list can be different!
        self.getKeysPerLevel()
        keysPerLevelBeforeInsert = self.keysPerLevel[:]
        self.keysPerLevelCopies.append([list(l) for l in keysPerLevelBeforeInsert])
        # edge list copy
        self.setEdgeList(self.rootNode)
        edgeListBeforeInsert = self.edgeList[:]
        self.edgeListCopies.append([list(l) for l in edgeListBeforeInsert])
        # num of nodes list copy
        nodePerLevelBefore = self.countNodesPerLevel()
        self.numOfNodesPerLevelCopies.append(nodePerLevelBefore)
        # use search to find node with key inside
        nodeWithKey = self.searchKey(key, nextNode)
        # check if node is root node
        # if root node call function for that
        if nodeWithKey == self.rootNode:
            deleted = True
            self.deleteKeyFromRoot(key)
        else:
            parent = self.getParent(nodeWithKey, self.rootNode)
            for index, child in enumerate(parent.children):
                if child == nodeWithKey:
                    childRef = index
            # if node has more than k + 1 keys, just delete it
            if len(nodeWithKey.keys) >= (self.k + 1) :
                indexOfKey = nodeWithKey.keys.index(key)
                nodeWithKey.keys.remove(key)
                deleted = True
                # take care of children!!!
                if not nodeWithKey.leaf:
                    self.takeCareOfChildren(nodeWithKey,indexOfKey)
            # Node will have underflow!
            else:
                if nodeWithKey.leaf:
                    deleted = True
                    # check if neighbours can give keys
                    leftNeighbour = self.getNodeWithId(self.rootNode, nodeWithKey.id - 1)
                    rightNeighbour = self.getNodeWithId(self.rootNode, nodeWithKey.id + 1)
                    if not leftNeighbour in parent.children:
                        leftNeighbour = None
                    if not rightNeighbour in parent.children:
                        rightNeighbour = None
                    # check if left neighbour can give key
                    if leftNeighbour is not None and len(leftNeighbour.keys) >= (self.k + 1):
                        # take key from left neighbour
                        # remove key from node
                        # results in underflow
                        nodeWithKey.keys.remove(key)
                        # key from parent which will be inserted to the underflow node
                        # - 1 because it is the left neighbour
                        fillKey = parent.keys[childRef - 1]
                        # key from neighbour which will be inserted into parent
                        # is always first value
                        borrowKey = leftNeighbour.keys[-1]
                        # remove borrow key from neighbour
                        leftNeighbour.keys.remove(borrowKey)
                        # insert borrow key into parent
                        # make space for one more key
                        i = len(parent.keys) - 1 
                        parent.keys.append(None)
                        if i == 0 and parent.keys[0] == None:
                            parent.keys[0] = borrowKey
                        else:
                            # compare every node key to insertion key 
                            while i >= 0 and borrowKey < parent.keys[i]: 
                                # shift key one place to the right
                                parent.keys[i + 1] = parent.keys[i] 
                                i -= 1
                            # insert key to correct place
                            parent.keys[i + 1] = borrowKey
                        # remove fill key from root
                        parent.keys.remove(fillKey)
                        # insert fill key into underflow node
                        # insert fill key into underflow node
                        # make space for one more key
                        i = len(nodeWithKey.keys) - 1 
                        nodeWithKey.keys.append(None)
                        if i == 0 and nodeWithKey.keys[0] == None:
                            nodeWithKey.keys[0] = fillKey
                        else:
                            # compare every node key to insertion key 
                            while i >= 0 and fillKey < nodeWithKey.keys[i]: 
                                # shift key one place to the right
                                nodeWithKey.keys[i + 1] = nodeWithKey.keys[i] 
                                i -= 1
                            # insert key to correct place
                            nodeWithKey.keys[i + 1] = fillKey
                        print('test')
                    elif rightNeighbour is not None and len(rightNeighbour.keys) >= (self.k + 1):
                        # remove key from node
                        # results in underflow
                        nodeWithKey.keys.remove(key)
                        # key from parent which will be inserted to the underflow node
                        fillKey = parent.keys[childRef]
                        # key from neighbour which will be inserted into parent
                        # is always first value
                        borrowKey = rightNeighbour.keys[0]
                        # remove borrow key from neighbour
                        rightNeighbour.keys.remove(borrowKey)
                        # insert borrow key into parent
                        # make space for one more key
                        i = len(parent.keys) - 1 
                        parent.keys.append(None)
                        if i == 0 and parent.keys[0] == None:
                            parent.keys[0] = borrowKey
                        else:
                            # compare every node key to insertion key 
                            while i >= 0 and borrowKey < parent.keys[i]: 
                                # shift key one place to the right
                                parent.keys[i + 1] = parent.keys[i] 
                                i -= 1
                            # insert key to correct place
                            parent.keys[i + 1] = borrowKey
                        # remove fill key from root
                        parent.keys.remove(fillKey)
                        # insert fill key into underflow node
                        # insert fill key into underflow node
                        # make space for one more key
                        i = len(nodeWithKey.keys) - 1 
                        nodeWithKey.keys.append(None)
                        if i == 0 and nodeWithKey.keys[0] == None:
                            nodeWithKey.keys[0] = fillKey
                        else:
                            # compare every node key to insertion key 
                            while i >= 0 and fillKey < nodeWithKey.keys[i]: 
                                # shift key one place to the right
                                nodeWithKey.keys[i + 1] = nodeWithKey.keys[i] 
                                i -= 1
                            # insert key to correct place
                            nodeWithKey.keys[i + 1] = fillKey
                        print('test')
                    # neighbours don't have enough keys -> merge
                    # merge with left neighbour 
                    elif leftNeighbour is not None:
                        # remove key from node
                        # results in underflow
                        nodeWithKey.keys.remove(key)
                        # all keys which will be merged into left neighbour
                        leftKeys = nodeWithKey.keys
                        # all left children
                        leftChildren = nodeWithKey.children
                        # key which goes from root into merged node
                        fillKey = parent.keys[childRef - 1]
                        # delete fill key from parent
                        parent.keys.remove(fillKey)
                        # delete underflow node
                        parent.children.remove(nodeWithKey)
                        # fill left neighbour
                        # first insert fill key
                        i = len(leftNeighbour.keys) - 1 
                        leftNeighbour.keys.append(None)
                        if i == 0 and leftNeighbour.keys[0] == None:
                            leftNeighbour.keys[0] = fillKey
                        else:
                            # compare every node key to insertion key 
                            while i >= 0 and fillKey < leftNeighbour.keys[i]: 
                                # shift key one place to the right
                                leftNeighbour.keys[i + 1] = leftNeighbour.keys[i] 
                                i -= 1
                            # insert key to correct place
                            leftNeighbour.keys[i + 1] = fillKey
                        # fill neighbour with every left key
                        for currentKey in leftKeys:
                            i = len(leftNeighbour.keys) - 1 
                            leftNeighbour.keys.append(None)
                            if i == 0 and leftNeighbour.keys[0] == None:
                                leftNeighbour.keys[0] = currentKey
                            else:
                                # compare every node key to insertion key 
                                while i >= 0 and currentKey < leftNeighbour.keys[i]: 
                                    # shift key one place to the right
                                    leftNeighbour.keys[i + 1] = leftNeighbour.keys[i] 
                                    i -= 1
                                # insert key to correct place
                                leftNeighbour.keys[i + 1] = currentKey
                        if len(leftChildren) == self.k + 1:
                            for key in leftChildren[1].keys:
                                leftChildren[0].keys.append(key)
                            del leftChildren[1]
                        # append all children
                        for currentChild in leftChildren:
                            leftNeighbour.children.append(currentChild)
                        print('test')
                        # parent is empty so delete it
                        if len(parent.keys) == 0 and parent == self.rootNode:
                            self.rootNode = leftNeighbour
                        self.updateNodeIds(self.rootNode)
                    elif rightNeighbour is not None:
                        # remove key from node
                        # results in underflow
                        nodeWithKey.keys.remove(key)
                        # all keys which will be merged into left neighbour
                        leftKeys = nodeWithKey.keys
                        # all left children
                        leftChildren = nodeWithKey.children
                        # key which goes from root into merged node
                        fillKey = parent.keys[childRef]
                        # delete fill key from parent
                        parent.keys.remove(fillKey)
                        # delete underflow node
                        parent.children.remove(nodeWithKey)
                        # fill left neighbour
                        # first insert fill key
                        i = len(rightNeighbour.keys) - 1 
                        rightNeighbour.keys.append(None)
                        if i == 0 and rightNeighbour.keys[0] == None:
                            rightNeighbour.keys[0] = fillKey
                        else:
                            # compare every node key to insertion key 
                            while i >= 0 and fillKey < rightNeighbour.keys[i]: 
                                # shift key one place to the right
                                rightNeighbour.keys[i + 1] = rightNeighbour.keys[i] 
                                i -= 1
                            # insert key to correct place
                            rightNeighbour.keys[i + 1] = fillKey
                        # fill neighbour with every left key
                        for currentKey in leftKeys:
                            i = len(rightNeighbour.keys) - 1 
                            rightNeighbour.keys.append(None)
                            if i == 0 and rightNeighbour.keys[0] == None:
                                rightNeighbour.keys[0] = currentKey
                            else:
                                # compare every node key to insertion key 
                                while i >= 0 and currentKey < rightNeighbour.keys[i]: 
                                    # shift key one place to the right
                                    rightNeighbour.keys[i + 1] = rightNeighbour.keys[i] 
                                    i -= 1
                                # insert key to correct place
                                rightNeighbour.keys[i + 1] = currentKey
                        if len(leftChildren) == self.k + 1:
                            for key in leftChildren[-1].keys:
                                leftChildren[-2].keys.append(key)
                            del leftChildren[-1]
                        # append all children
                        temp = 0
                        for currentChild in leftChildren:
                            rightNeighbour.children.insert(temp,currentChild)
                            temp += 1
                        print('test')
                        # parent is empty so delete it
                        if not parent.keys and parent == self.rootNode:
                            self.rootNode = rightNeighbour
                        self.updateNodeIds(self.rootNode)
                else:
                    # root with only one key
                    if len(parent.keys) == 1:
                        # check if neighbours can give keys
                        leftNeighbour = self.getNodeWithId(self.rootNode, nodeWithKey.id - 1)
                        rightNeighbour = self.getNodeWithId(self.rootNode, nodeWithKey.id + 1)
                        if not leftNeighbour in parent.children:
                            leftNeighbour = None
                        if not rightNeighbour in parent.children:
                            rightNeighbour = None
                        indexOfKey = nodeWithKey.keys.index(key)
                        nodeWithKey.keys.remove(key)
                        deleted = True
                        # left neighbour can give key
                        if not leftNeighbour is None and len(leftNeighbour.keys) >= self.k + 1:
                            borrowKey = leftNeighbour.children[-1].keys[-1]
                            indexOfLastKey = len(leftNeighbour.keys) - 1
                            del leftNeighbour.children[-1].keys[-1]
                            leftNeighbour.children[-1].keys.insert(0, leftNeighbour.keys[-1])
                            del leftNeighbour.keys[-1]
                            self.takeCareOfChildren(leftNeighbour,indexOfLastKey)
                            rootKey = parent.keys[0]
                            parent.keys.insert(0,borrowKey)
                            parent.keys.remove(rootKey)
                            biggestKey = nodeWithKey.children[indexOfKey].keys[-1]
                            index = nodeWithKey.children[indexOfKey].keys.index(biggestKey)
                            nodeWithKey.children[0].keys.insert(0, rootKey)
                            changeKey = nodeWithKey.children[0].keys[-1]
                            nodeWithKey.children[0].keys.remove(changeKey)
                            nodeWithKey.keys.insert(0, changeKey)
                            if indexOfKey >= len(nodeWithKey.keys) - 1:
                                del nodeWithKey.children[indexOfKey].keys[-1]
                                nodeWithKey.children[indexOfKey].keys.insert(0,nodeWithKey.keys[indexOfKey])
                                del nodeWithKey.keys[indexOfKey]
                                nodeWithKey.keys.append(biggestKey)
                        # right neighbour can give key
                        elif not rightNeighbour is None and len(rightNeighbour.keys) >= self.k + 1:
                            borrowKey = rightNeighbour.children[0].keys[0]
                            del rightNeighbour.children[0].keys[0]
                            rightNeighbour.children[0].keys.append(rightNeighbour.keys[0])
                            del rightNeighbour.keys[0]
                            self.takeCareOfChildren(rightNeighbour,0)
                            rootKey = parent.keys[0]
                            parent.keys.insert(0,borrowKey)
                            parent.keys.remove(rootKey)
                            biggestKey = nodeWithKey.children[-1].keys[0]
                            index = nodeWithKey.children[-1].keys.index(biggestKey)
                            nodeWithKey.children[-1].keys.append(rootKey)
                            changeKey = nodeWithKey.children[indexOfKey + 1].keys[0]
                            nodeWithKey.children[indexOfKey + 1].keys.remove(changeKey)
                            nodeWithKey.keys.insert(indexOfKey, changeKey)
                            if indexOfKey < len(nodeWithKey.keys) - 1:
                                del nodeWithKey.children[-1].keys[0]
                                nodeWithKey.children[indexOfKey + 1].keys.append(nodeWithKey.keys[indexOfKey + 1])
                                del nodeWithKey.keys[indexOfKey + 1]
                                nodeWithKey.keys.insert(indexOfKey + 1, biggestKey)
                            print('test')
                        # merge with neighbour
                        else:
                            # check which node is not none
                            if not leftNeighbour is None:
                                mergeNode = leftNeighbour
                                mergeNode.keys.append(parent.keys[0])
                                leftKeys = nodeWithKey.keys
                                leftChildren = nodeWithKey.children
                                lastChild = mergeNode.children[-1]
                                firstChild = nodeWithKey.children[0]
                                for key in leftKeys:
                                    mergeNode.keys.append(key)
                                for key in firstChild.keys:
                                    lastChild.keys.append(key)
                                for child in leftChildren:
                                    mergeNode.children.append(child)
                                mergeNode.children.remove(firstChild)
                                self.rootNode = mergeNode
                                self.updateNodeIds(self.rootNode)
                            else:
                                mergeNode = rightNeighbour
                                nodeWithKey.keys.append(parent.keys[0])
                                leftKeys = mergeNode.keys
                                leftChildren = mergeNode.children
                                lastChild = nodeWithKey.children[-1]
                                firstChild = mergeNode.children[0]
                                for key in leftKeys:
                                    nodeWithKey.keys.append(key)
                                for key in firstChild.keys:
                                    lastChild.keys.append(key)
                                for child in leftChildren:
                                    nodeWithKey.children.append(child)
                                nodeWithKey.children.remove(firstChild)
                                self.rootNode = nodeWithKey
                                self.updateNodeIds(self.rootNode)
        # set keys per level list -> has to be copy of list because every key list can be different!
        self.getKeysPerLevel()
        keysPerLevelBeforeInsert = self.keysPerLevel[:]
        self.keysPerLevelCopies.append([list(l) for l in keysPerLevelBeforeInsert])
        # edge list copy
        self.setEdgeList(self.rootNode)
        edgeListBeforeInsert = self.edgeList[:]
        self.edgeListCopies.append([list(l) for l in edgeListBeforeInsert])
        # num of nodes list copy
        nodePerLevelBefore = self.countNodesPerLevel()
        self.numOfNodesPerLevelCopies.append(nodePerLevelBefore)
        return deleted
    
    def deleteKeyFromRoot(self, key):
        # root has no children so just remove key
        if not self.rootNode.children:
            self.rootNode.keys.remove(key)
        else:
            # root node has only one key
            if len(self.rootNode.keys) == 1:
                keyIndex = self.rootNode.keys.index(key)
                del self.rootNode.keys[keyIndex]
                mergeChild = self.rootNode.children[keyIndex]
                otherChild = self.rootNode.children[keyIndex + 1]
                if mergeChild.leaf:
                    if len(mergeChild.keys) >= self.k + 1:
                        borrowKey = mergeChild.keys[-1]
                        mergeChild.keys.remove(borrowKey)
                        self.rootNode.keys.insert(keyIndex,borrowKey)
                    elif len(otherChild.keys) >= self.k + 1:
                        borrowKey = otherChild.keys[0]
                        otherChild.keys.remove(borrowKey)
                        self.rootNode.keys.insert(keyIndex,borrowKey)
                    else:
                        # merge both children
                        # left child will be new root
                        newRoot = self.rootNode.children[0]
                        # take all keys from right child
                        leftKeys = self.rootNode.children[1].keys
                        for key in leftKeys:
                            newRoot.keys.append(key)
                        self.rootNode = newRoot
                        self.updateNodeIds(self.rootNode)
                elif len(mergeChild.keys) >= self.k + 1:
                    borrowKey = mergeChild.children[-1].keys[-1]
                    lastKey = mergeChild.keys[-1]
                    lastIndex = mergeChild.keys.index(lastKey)
                    del mergeChild.children[-1].keys[-1]
                    self.rootNode.keys.insert(keyIndex,borrowKey)
                    if len(mergeChild.children[-1].keys) < self.k:
                        keyFromParent = mergeChild.keys[-1]
                        mergeChild.children[-1].keys.insert(0, keyFromParent)
                        del mergeChild.keys[-1]
                        self.takeCareOfChildren(mergeChild,lastIndex)
                    if not mergeChild.children[-1].leaf:
                        self.takeCareOfChildren(mergeChild,lastIndex)
                elif len(otherChild.keys) >= self.k + 1:
                    borrowKey = otherChild.children[0].keys[0]
                    lastIndex = otherChild.children[0].keys.index(borrowKey)
                    del otherChild.children[0].keys[0]
                    self.rootNode.keys.insert(keyIndex,borrowKey)
                    if len(otherChild.children[0].keys) < self.k:
                        keyFromParent = otherChild.keys[0]
                        otherChild.children[0].keys.append(keyFromParent)
                        del otherChild.keys[0]
                        self.takeCareOfChildren(otherChild,0)
                    if not otherChild.children[0]:
                        self.takeCareOfChildren(otherChild.children[0], 0)
                elif len(mergeChild.children[-1].keys) >= self. k + 1:
                    borrowKey = mergeChild.children[-1].keys[-1]
                    lastIndex = mergeChild.children[-1].keys.index(borrowKey)
                    del mergeChild.children[-1].keys[-1]
                    self.rootNode.keys.insert(keyIndex,borrowKey)
                    del mergeChild.children[-1].keys[0]
                    if len(mergeChild.children[-1].keys) < self.k:
                        keyFromParent = mergeChild.keys[-1]
                        indexFromParent = mergeChild.keys.index(keyFromParent)
                        mergeChild.children[-1].keys.insert(0,keyFromParent)
                        del mergeChild.keys[0]
                        self.takeCareOfChildren(mergeChild,indexFromParent)
                    if not mergeChild.children[-1].leaf:
                        self.takeCareOfChildren(mergeChild.children[-1], 0)
                elif len(otherChild.children[0].keys) >= self.k + 1:
                    borrowKey = otherChild.children[0].keys[0]
                    del otherChild.children[0].keys[0]
                    self.rootNode.keys.insert(keyIndex,borrowKey)
                    if len(otherChild.children[0].keys) < self.k:
                        keyFromParent = otherChild.keys[0]
                        otherChild.children[0].keys.append(keyFromParent)
                        del otherChild.keys[0]
                        self.takeCareOfChildren(otherChild,0)
                    if not otherChild.children[0].leaf:
                        self.takeCareOfChildren(otherChild.children[0], 0)
                else:
                    # merge both children
                    # left child will be new root
                    newRoot = self.rootNode.children[0]
                    # take all keys from right child
                    leftKeys = self.rootNode.children[1].keys
                    # take all children from right child
                    # the last of first node and the first of second node will be merged!
                    lastChildOfMerge = self.rootNode.children[0].children[-1]
                    firstChildOfMerge = self.rootNode.children[1].children[0]
                    #self.rootNode.children[1].children.remove(firstChildOfMerge)
                    leftChildren = self.rootNode.children[1].children
                    # fill neighbour with every left key
                    for currentKey in leftKeys:
                        i = len(newRoot.keys) - 1 
                        newRoot.keys.append(None)
                        if i == 0 and newRoot.keys[0] == None:
                            newRoot.keys[0] = currentKey
                        else:
                            # compare every node key to insertion key 
                            while i >= 0 and currentKey < newRoot.keys[i]: 
                                # shift key one place to the right
                                newRoot.keys[i + 1] = newRoot.keys[i] 
                                i -= 1
                            # insert key to correct place
                            newRoot.keys[i + 1] = currentKey 
                    # give new root every child of right child
                    for currentChild in leftChildren:
                        newRoot.children.append(currentChild)
                    # merge together
                    for key in firstChildOfMerge.keys:
                        lastChildOfMerge.keys.append(key)
                    del newRoot.children[self.k + 1]
                    self.rootNode = newRoot
                    self.updateNodeIds(self.rootNode)
            # root has more than 1 key
            else:
                keyIndex = self.rootNode.keys.index(key)
                del self.rootNode.keys[keyIndex]
                mergeChild = self.rootNode.children[keyIndex]
                otherChild = self.rootNode.children[keyIndex + 1]
                if len(mergeChild.keys) >= self.k + 1:
                    borrowKey = mergeChild.keys[-1]
                    lastIndex = mergeChild.keys.index(borrowKey)
                    del mergeChild.keys[-1]
                    self.rootNode.keys.insert(keyIndex,borrowKey)
                    if not mergeChild.leaf:
                        self.takeCareOfChildren(mergeChild,lastIndex)
                elif len(otherChild.keys) >= self.k + 1:
                    borrowKey = otherChild.keys[0]
                    firstIndex = otherChild.keys.index(borrowKey)
                    del otherChild.keys[0]
                    self.rootNode.keys.insert(keyIndex,borrowKey)
                    if not otherChild.leaf:
                        self.takeCareOfChildren(otherChild,firstIndex)
                else:
                    leftKeys = otherChild.keys
                    leftChildren = otherChild.children
                    if not otherChild.leaf:
                        firstChildOfMerge = otherChild.children[0]
                    # delete other child
                    del self.rootNode.children[keyIndex + 1]
                    # fill merge child with every left key
                    for currentKey in leftKeys:
                        i = len(mergeChild.keys) - 1 
                        mergeChild.keys.append(None)
                        if i == 0 and mergeChild.keys[0] == None:
                            mergeChild.keys[0] = currentKey
                        else:
                            # compare every node key to insertion key 
                            while i >= 0 and currentKey < mergeChild.keys[i]: 
                                # shift key one place to the right
                                mergeChild.keys[i + 1] = mergeChild.keys[i] 
                                i -= 1
                            # insert key to correct place
                            mergeChild.keys[i + 1] = currentKey
                    if not otherChild.leaf:
                        for key in firstChildOfMerge.keys:
                            mergeChild.children[-1].keys.append(key)
                        for child in leftChildren:
                            mergeChild.children.append(child)
                        mergeChild.children.remove(firstChildOfMerge)
                    self.updateNodeIds(self.rootNode)
                    print('test')


    

    def borrowKeyFromNeighbour(self, node):
        # check if neighbours can give keys
        parent = self.getParent(node, self.rootNode)
        leftNeighbour = self.getNodeWithId(self.rootNode, node.id - 1)
        rightNeighbour = self.getNodeWithId(self.rootNode, node.id + 1)
        # check if nodes are really neighbours
        if not leftNeighbour is None:
            if not leftNeighbour in parent.children:
                leftNeighbour = None
        if not rightNeighbour is None:
            if not rightNeighbour in parent.children:
                rightNeighbour = None
        for index, child in enumerate(parent.children):
            if child == node:
                childRef = index
        if not node == self.rootNode:
            # check if left neighbour can give key
            if leftNeighbour is not None and len(leftNeighbour.keys) >= (self.k + 1):
                # take key from left neighbour
                # key from parent which will be inserted to the underflow node
                # - 1 because it is the left neighbour
                fillKey = parent.keys[childRef - 1]
                # key from neighbour which will be inserted into parent
                # is always first value
                borrowKey = leftNeighbour.keys[-1]
                # get ref which belongs to the node
                childOfBorrowKey = rightNeighbour.children[-1]
                rightNeighbour.children.remove(childOfBorrowKey)
                node.children.insert(0, childOfBorrowKey)
                # remove borrow key from neighbour
                leftNeighbour.keys.remove(borrowKey)
                # insert borrow key into parent
                # make space for one more key
                i = len(parent.keys) - 1 
                parent.keys.append(None)
                if i == 0 and parent.keys[0] == None:
                    parent.keys[0] = borrowKey
                else:
                    # compare every node key to insertion key 
                    while i >= 0 and borrowKey < parent.keys[i]: 
                        # shift key one place to the right
                        parent.keys[i + 1] = parent.keys[i] 
                        i -= 1
                    # insert key to correct place
                    parent.keys[i + 1] = borrowKey
                # remove fill key from root
                parent.keys.remove(fillKey)
                # insert fill key into underflow node
                # insert fill key into underflow node
                # make space for one more key
                i = len(node.keys) - 1 
                node.keys.append(None)
                if i == 0 and node.keys[0] == None:
                    node.keys[0] = fillKey
                else:
                    # compare every node key to insertion key 
                    while i >= 0 and fillKey < node.keys[i]: 
                        # shift key one place to the right
                        node.keys[i + 1] = node.keys[i] 
                        i -= 1
                    # insert key to correct place
                    node.keys[i + 1] = fillKey
                print('test')
            elif rightNeighbour is not None and len(rightNeighbour.keys) >= (self.k + 1):
                # key from parent which will be inserted to the underflow node
                fillKey = parent.keys[childRef]
                # key from neighbour which will be inserted into parent
                # is always first value
                borrowKey = rightNeighbour.keys[0]
                # remove borrow key from neighbour
                rightNeighbour.keys.remove(borrowKey)
                # get ref which belongs to the node
                childOfBorrowKey = rightNeighbour.children[0]
                rightNeighbour.children.remove(childOfBorrowKey)
                node.children.append(childOfBorrowKey)
                # insert borrow key into parent
                # make space for one more key
                i = len(parent.keys) - 1 
                parent.keys.append(None)
                if i == 0 and parent.keys[0] == None:
                    parent.keys[0] = borrowKey
                else:
                    # compare every node key to insertion key 
                    while i >= 0 and borrowKey < parent.keys[i]: 
                        # shift key one place to the right
                        parent.keys[i + 1] = parent.keys[i] 
                        i -= 1
                    # insert key to correct place
                    parent.keys[i + 1] = borrowKey
                # remove fill key from root
                parent.keys.remove(fillKey)
                # insert fill key into underflow node
                # insert fill key into underflow node
                # make space for one more key
                i = len(node.keys) - 1 
                node.keys.append(None)
                if i == 0 and node.keys[0] == None:
                    node.keys[0] = fillKey
                else:
                    # compare every node key to insertion key 
                    while i >= 0 and fillKey < node.keys[i]: 
                        # shift key one place to the right
                        node.keys[i + 1] = node.keys[i] 
                        i -= 1
                    # insert key to correct place
                    node.keys[i + 1] = fillKey
                print('test')
                return True
        return False
    
    def mergeNode(self, node):
        parent = self.getParent(node,self.rootNode)
        leftNeighbour = self.getNodeWithId(self.rootNode, node.id - 1)
        rightNeighbour = self.getNodeWithId(self.rootNode, node.id + 1)
        # check if nodes are really neighbours
        if not leftNeighbour in parent.children:
            leftNeighbour = None
        if not rightNeighbour in parent.children:
            rightNeighbour = None
        for index, child in enumerate(parent.children):
            if child == node:
                childRef = index
            # merge with left neighbour 
            if leftNeighbour is not None:
                # all keys which will be merged into left neighbour
                leftKeys = node.keys
                # key which goes from root into merged node
                fillKey = parent.keys[childRef - 1]
                # delete fill key from parent
                parent.keys.remove(fillKey)
                # delete underflow node
                parent.children.remove(node)
                # fill left neighbour
                # first insert fill key
                i = len(leftNeighbour.keys) - 1 
                leftNeighbour.keys.append(None)
                if i == 0 and leftNeighbour.keys[0] == None:
                    leftNeighbour.keys[0] = fillKey
                else:
                    # compare every node key to insertion key 
                    while i >= 0 and fillKey < leftNeighbour.keys[i]: 
                        # shift key one place to the right
                        leftNeighbour.keys[i + 1] = leftNeighbour.keys[i] 
                        i -= 1
                    # insert key to correct place
                    leftNeighbour.keys[i + 1] = fillKey
                # fill neighbour with every left key
                for currentKey in leftKeys:
                    i = len(leftNeighbour.keys) - 1 
                    leftNeighbour.keys.append(None)
                    if i == 0 and leftNeighbour.keys[0] == None:
                        leftNeighbour.keys[0] = currentKey
                    else:
                        # compare every node key to insertion key 
                        while i >= 0 and currentKey < leftNeighbour.keys[i]: 
                            # shift key one place to the right
                            leftNeighbour.keys[i + 1] = leftNeighbour.keys[i] 
                            i -= 1
                        # insert key to correct place
                        leftNeighbour.keys[i + 1] = currentKey
                print('test')
                # parent is empty so delete it
                if parent.keys == 0:
                    self.rootNode = leftNeighbour
                self.updateNodeIds(self.rootNode)
            elif rightNeighbour is not None:
                # all keys which will be merged into left neighbour
                leftKeys = node.keys
                # key which goes from root into merged node
                fillKey = parent.keys[childRef]
                # delete fill key from parent
                parent.keys.remove(fillKey)
                # delete underflow node
                parent.children.remove(node)
                # fill left neighbour
                # first insert fill key
                i = len(rightNeighbour.keys) - 1 
                rightNeighbour.keys.append(None)
                if i == 0 and rightNeighbour.keys[0] == None:
                    rightNeighbour.keys[0] = fillKey
                else:
                    # compare every node key to insertion key 
                    while i >= 0 and fillKey < rightNeighbour.keys[i]: 
                        # shift key one place to the right
                        rightNeighbour.keys[i + 1] = rightNeighbour.keys[i] 
                        i -= 1
                    # insert key to correct place
                    rightNeighbour.keys[i + 1] = fillKey
                # fill neighbour with every left key
                for currentKey in leftKeys:
                    i = len(rightNeighbour.keys) - 1 
                    rightNeighbour.keys.append(None)
                    if i == 0 and rightNeighbour.keys[0] == None:
                        rightNeighbour.keys[0] = currentKey
                    else:
                        # compare every node key to insertion key 
                        while i >= 0 and currentKey < rightNeighbour.keys[i]: 
                            # shift key one place to the right
                            rightNeighbour.keys[i + 1] = rightNeighbour.keys[i] 
                            i -= 1
                        # insert key to correct place
                        rightNeighbour.keys[i + 1] = currentKey
                print('test')

    def takeCareOfChildren(self,node,index):
        smallerChild = node.children[index]
        greaterChild = node.children[index + 1] 
        if len(node.keys) < self.k:
            parentOfNode = self.getParent(node, self.rootNode)
            idOfNode = parentOfNode.children.index(node)
            leftNeighbour = self.getNodeWithId(self.rootNode, node.id -1)
            rightNeighbour = self.getNodeWithId(self.rootNode, node.id +1)
            # check if nodes are really neighbours
            if not leftNeighbour in parentOfNode.children:
                leftNeighbour = None
            if not rightNeighbour in parentOfNode.children:
                rightNeighbour = None
            if not leftNeighbour is None:
                if len(leftNeighbour.keys) >= self.k + 1:
                    borrowKey = leftNeighbour.keys[-1]
                    lastIndex = leftNeighbour.keys.index(borrowKey)
                    del leftNeighbour.keys[-1]
                    keyOfParent = parentOfNode.keys[idOfNode]
                    del parentOfNode.keys[idOfNode]
                    parentOfNode.keys.insert(idOfNode,borrowKey)
                    node.keys.insert(index,keyOfParent)
                    if not leftNeighbour.leaf:
                        self.takeCareOfChildren(leftNeighbour,lastIndex)
                else:
                    print('merge')
            else:
                if len(rightNeighbour.keys) >= self.k + 1:
                    borrowKey = rightNeighbour.keys[0]
                    firstIndex = rightNeighbour.keys.index(borrowKey)
                    del rightNeighbour.keys[0]
                    keyOfParent = parentOfNode.keys[idOfNode]
                    del parentOfNode.keys[idOfNode]
                    parentOfNode.keys.insert(idOfNode,borrowKey)
                    node.keys.insert(index,keyOfParent)
                    if not rightNeighbour.leaf:
                        self.takeCareOfChildren(rightNeighbour,firstIndex)
                else:
                    print('merge')
        elif len(smallerChild.keys) >= self.k + 1:
            borrowKey = smallerChild.keys[-1]
            indexOfBorrowKey = smallerChild.keys.index(borrowKey)
            del smallerChild.keys[-1]
            node.keys.insert(index,borrowKey)
            # check if children have to be fixed
            if not smallerChild.leaf:
                self.takeCareOfChildren(smallerChild,indexOfBorrowKey)
        elif len(greaterChild.keys) >= self.k + 1:
            borrowKey = greaterChild.keys[0]
            indexOfBorrowKey = greaterChild.keys.index(borrowKey)
            del greaterChild.keys[0]
            node.keys.insert(index,borrowKey)
            # check if children have to be fixed
            if not greaterChild.leaf:
                self.takeCareOfChildren(greaterChild,indexOfBorrowKey)
        # merge 
        else:
            leftKeys = greaterChild.keys
            for currentKey in leftKeys:
                i = len(smallerChild.keys) - 1 
                smallerChild.keys.append(None)
                if i == 0 and smallerChild.keys[0] == None:
                    smallerChild.keys[0] = currentKey
                else:
                    # compare every node key to insertion key 
                    while i >= 0 and currentKey < smallerChild.keys[i]: 
                        # shift key one place to the right
                        smallerChild.keys[i + 1] = smallerChild.keys[i] 
                        i -= 1
                    # insert key to correct place
                    smallerChild.keys[i + 1] = currentKey
            node.children.remove(greaterChild)
            self.updateNodeIds(self.rootNode)
            if not greaterChild.leaf:
                leftChildren = greaterChild.children
                for child in leftChildren:
                    node.children.append(child)






    # search key in node
    # go through node and check if key is there
    # if not and node has no children -> key is not in the tree
    # if node has children go to child node with current index i
    def searchKey(self, key, nextNode = None):
        self.searchedNodes.append(nextNode.id)
        i = 0
        # go through node and check at which point key is smaller
        while i < len(nextNode.keys) and key > nextNode.keys[i]: 
            i += 1
        if i < len(nextNode.keys) and key == nextNode.keys[i]:
            return nextNode
        # if keys is not found and node is a leaf -> key is not in the tree
        elif nextNode.leaf: 
            return None
        #go to node in which key maybe is 
        return self.searchKey(key, nextNode.children[i])
    
    def getNodeWithId(self, startNode, nodeId):
        if startNode.id == nodeId:
            return startNode
        else:
            for child in startNode.children:
                result = self.getNodeWithId(child, nodeId)
                if result is not None:
                    return result



    # print tree
    def printTree(self, node, level = 0):
        print("Level ", level, " Anzahl Schlüssel ", len(node.keys))
        for i in node.keys:
            print(i)
        print()
        level += 1
        if len(node.children) > 0:
            for i in node.children:
                self.printTree(i, level)

    # function returns list for frontend which contains numbers of nodes per level
    # at index 0 -> root level, but the list has to be reveresed so the frontend can work with it
    def countNodesPerLevel(self):
        levels = []
        self.countNodesPerLevelHelp(self.rootNode, 0, levels)
        levels.reverse()
        return levels

    def countNodesPerLevelHelp(self, node, level, levels):
        if level == len(levels):
            levels.append(0)
        levels[level] += 1
        for child in node.children:
            self.countNodesPerLevelHelp(child, level + 1, levels)


    # function that counts the numbers of levels the tree has for the list which will be sent to the frontend
    # level 1 -> root
    def getNumOfLevels(self, node, level = 0):
        self.levels += 1
        if not node.leaf:
            self.getNumOfLevels(node.children[0])

    
    # prepares the node list per level
    # for each level it adds one index
    def initNodeList(self):
        for i in range(self.levels):
            self.numOfNodesPerLevel.append(0)


    # frontend needs the node list with root at the last index
    # function simply revereses the created node list so the root is at the last index
    def prepareNodeList(self):
        return self.numOfNodesPerLevel.reverse()
    
    # function that returns keys per level 
    # useses reverse level order traversal of the tree
    def getKeysPerLevel(self):
        self.keysPerLevel = []
        if self.rootNode is None:
            return
        # create an empty queue and enqueue the root node
        queue = deque()
        queue.append(self.rootNode)
        # create a stack to reverse level order nodes
        stack = deque()
        # loop till queue is empty
        while queue:
            # process each node in the queue and enqueue their children
            curr = queue.popleft()
            # push the current node into the stack
            stack.append(curr)
            # it is important to process the right node before the left node
            for child in reversed(curr.children):
                queue.append(child)
        # pop all nodes from the stack and print them
        while stack:
            currentNode = stack.pop()
            self.keysPerLevel.append(currentNode.keys)
            for i in currentNode.children:
                # search every child node from current node from left to right 
                queue.append(i)
    

    # nodes have an ID, frontend needs from lowest level left to right upwards the IDs incremented
    # -> leftest leaf of the tree has ID 0, node right to it 1 and so on
    # this function updates the node IDs
    # it useses reverse level order traversal
    def updateNodeIds(self, node):
        # variable for id
        i = 0
        if self.rootNode is None:
            return
        # create an empty queue and enqueue the root node
        queue = deque()
        queue.append(self.rootNode)
        # create a stack to reverse level order nodes
        stack = deque()
        # loop till queue is empty
        while queue:
            # process each node in the queue and enqueue their children
            curr = queue.popleft()
            # push the current node into the stack
            stack.append(curr)
            # it is important to process the right node before the left node
            for child in reversed(curr.children):
                queue.append(child)
        # pop all nodes from the stack and print them
        while stack:
            #print(stack.pop(), end=' ')
            currentNode = stack.pop()
            currentNode.id = i
            i += 1
            self.nodeIds.append(currentNode.id)

    def setEdgeList(self, node):
        res = []
        if self.rootNode is None:
            return
        # create an empty queue and enqueue the root node
        queue = deque()
        queue.append(self.rootNode)
        # create a stack to reverse level order nodes
        stack = deque()
        # loop till queue is empty
        while queue:
            # process each node in the queue and enqueue their children
            curr = queue.popleft()
            # push the current node into the stack
            stack.append(curr)
            # it is important to process the right node before the left node
            for child in reversed(curr.children):
                queue.append(child)
        # pop all nodes from the stack and print them
        while stack:
            #print(stack.pop(), end=' ')
            currentNode = stack.pop()
            temp = []
            for child in currentNode.children:
                temp.append(child.id)
            res.append(temp)
        edgeListCopy = res[:]
        self.edgeList = edgeListCopy



    def getTreeListForSearch(self):
        # create a tree list for searching
        # tree list is made of nodes per level, keys per level and edges
        treeList = []
        keysPerLevelCopies = []
        numOfNodesPerLevel = self.countNodesPerLevel()
        self.getKeysPerLevel()
        keysPerLevel = self.keysPerLevel[:]
        keysPerLevelCopies.append([list(l) for l in keysPerLevel])
        self.setEdgeList(self.rootNode)
        edgeList = self.edgeList[:]
        # temp list for tree list
        temp = []
        temp.append(numOfNodesPerLevel)
        temp.append(keysPerLevel)
        temp.append(edgeList)
        treeList.append(temp)
        return treeList
    

    def reset(self):
        # make new root and update all attributes
        newRoot = node.Node(True)
        self.rootNode = newRoot
        treeList = []
        keysPerLevelCopies = []
        numOfNodesPerLevel = self.countNodesPerLevel()
        self.getKeysPerLevel()
        keysPerLevel = self.keysPerLevel[:]
        keysPerLevelCopies.append([list(l) for l in keysPerLevel])
        self.setEdgeList(self.rootNode)
        edgeList = self.edgeList[:]
        # temp list for tree list
        temp = []
        temp.append(numOfNodesPerLevel)
        temp.append(keysPerLevel)
        temp.append(edgeList)
        treeList = temp
        return treeList

