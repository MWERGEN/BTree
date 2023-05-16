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
from node import Node
from collections import deque

class BTree:
    def __init__(self, k):
        self.rootNode = Node(True)
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
        #case 1
        # node can hold 2 * order keys
        if len(root.keys) == 2 * self.k:
            # check if root has children
            if not root.children: 
                # new root node
                temp = Node()
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
                self.splitNode(temp, key,0) 
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
                # check if node where key should go is full -> children[i] means all keys in this node are smaller!
                if len(root.children[i].keys) == (2 * self.k): 
                    # split node to make room for new key 
                    self.splitNode(root, key,i) 
                    test = True
                    #if key > root.keys[i]:
                    #   i += 1
                if not test:
                    self.insertNotFull(root.children[i], key, source, target, False)
        # case2
        else:
            # just insert key into node 
            self.insertNotFull(root,key, source, target,False) 
            # key is inserted so animation is over -> 0
            self.animationList.append(0)
            self.usedReferences.append(0)
            


    # split child node at index i of parent
    # parent will have middle key of splitNode
    # splitNode will have all keys which are smaller than parents
    # newNode will have all keys which are greater than parents
    def splitNode(self, parent, key, index):
        #source = []
        #target = []
        k = self.k
        self.updateNodeIds(self.rootNode)
        source = parent.children[0].id
        target = parent.id 
        self.visitiedNodes[0].append(source)
        self.visitiedNodes[1].append(target)
        # full node
        splitNode = parent.children[index]
        # second node where are all keys which are greater than the middle key will go
        newNode = Node(splitNode.leaf) 
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
        self.animationList.append(1)
        middleIndex = int(len(splitNode.keys) / 2)
        # add reference to node which holds all greater keys
        parent.children.insert(index + 1, newNode) 
        # fill parent with splitkey -> middle key
        self.insertNotFull(parent,splitNode.keys[middleIndex], source, target, True)
        # used key is inserted key
        self.usedKeys.append(splitNode.keys[middleIndex])
        del splitNode.keys[middleIndex]
        # take all greater keys and insert them from order to 2 * order - 1
        newNode.keys = splitNode.keys[middleIndex: 2 * k] 
        # take all smaller keys and insert them from 0 to order - 1
        splitNode.keys = splitNode.keys[0: middleIndex] 
        if not splitNode.leaf:
            # give newNode with all greater keys all references to all greater children
            newNode.children = splitNode.children[k: 2 * k] 
            # updte references to only smaller children
            splitNode.children = splitNode.children[0: k - 1]
        if len(parent.keys) == (2 * self.k ) + 1:
            # root is full -> new root
            if parent is self.rootNode:
                # new root node
                temp = Node()
                # reference to child which will hold all smaller keys!
                temp.children.insert(0, parent) 
                self.rootNode = temp
                # split the full node
                self.splitRoot(temp,0) 
                #self.insertNotFull(temp,key, source, target)
                # key is inserted so animation is over -> 0
                self.animationList.append(0)
                # there is a new node in the tree so update the ids of the nodes
                # this ensures that at every operation the node ids are correct
                self.updateNodeIds(self.rootNode)
            # parent is full
            else:
                rootOfParent = self.getParent(parent, self.rootNode)
                loopIndex = 0
                indexOfSplit = 0
                for i in rootOfParent.children:
                    loopIndex += 1
                    if i == parent:
                        indexOfSplit = loopIndex
                indexOfSplit -= 1
                self.splitRoot(rootOfParent,indexOfSplit)


    def splitRoot(self, parent, index):
        source = []
        target = []
        k = self.k
        # full node
        splitNode = parent.children[index]
        # second node where are all keys which are greater than the middle key will go
        newNode = Node(splitNode.leaf) 
        i = len(splitNode.keys) - 1
        middleIndex = int(len(splitNode.keys) / 2)
        # add reference to node which holds all greater keys
        parent.children.insert(index + 1, newNode) 
        # fill parent with splitkey -> middle key
        self.insertNotFull(parent,splitNode.keys[middleIndex], source, target, True)
        del splitNode.keys[middleIndex]
        # take all greater keys and insert them from order to 2 * order - 1
        newNode.keys = splitNode.keys[middleIndex: 2 * k] 
        # take all smaller keys and insert them from 0 to order - 1
        splitNode.keys = splitNode.keys[0: middleIndex] 
        # give newNode with all greater keys all references to all greater children
        newNode.children = splitNode.children[k + 1: 2 * k + 2] 
        # updte references to only smaller children
        splitNode.children = splitNode.children[0: k + 1]

    def getParent(self, searchNode, rootNode):
        if searchNode in rootNode.children:
            return rootNode
        if len(rootNode.children) > 0:
            for i in rootNode.children:
                self.getParent(searchNode,i)
        else:
            return None
        


    # insert key into not full node
    # there are two cases:
    # 1. if node is leaf -> find correct place to insert and insert
    # 2. if node is not a leaf -> find correct node 
    def insertNotFull(self, node, key, source, target, fromSplit):
            test = False
            emptyNode = False
            if len(node.keys) == 0:
                i = 0
                emptyNode = True
            else:
                i = len(node.keys) - 1 
            if node.leaf or fromSplit:
                if emptyNode:
                    node.keys.append(key)
                    self.animationList.append(1)
                    self.usedKeys.append(key)
                    # get the current keys per level of the tree
                    nodePerLevelBefore = self.countNodesPerLevel()
                    self.numOfNodesPerLevelCopies.append(nodePerLevelBefore)
                    if not fromSplit:
                        # edge list copy
                        self.setEdgeList(self.rootNode)
                        edgeListBeforeInsert = self.edgeList[:]
                        self.edgeListCopies.append([list(l) for l in edgeListBeforeInsert])
                        self.usedReferences.append(0)
                        # get the current keys per level of the tree
                        self.getKeysPerLevel()
                        keysPerLevelBeforeInsert = self.keysPerLevel[:]
                        self.keysPerLevelCopies.append([list(l) for l in keysPerLevelBeforeInsert])
                else:
                    # make space for one more key
                    node.keys.append(None)
                    if i == 0 and node.keys[0] == None:
                        node.keys[0] = key
                    else:
                        # compare every node key to insertion key 
                        while i >= 0 and key < node.keys[i]: 
                            # shift key one place to the right
                            node.keys[i + 1] = node.keys[i] 
                            i -= 1
                        # insert key to correct place
                        node.keys[i + 1] = key
                        source.append(source[0])
                        target.append(node.id)
                    # animation for comparing 
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
                    # check if node where key should go is full -> children[i] means all keys in this node are smaller!
                    if not node.children[i].children:
                        if len(node.children[i].keys) == (2 * self.k): 
                            # split node to make room for new key 
                            self.splitNode(node, key,i) 
                            test = True
                            #if key > node.keys[i]:
                             #   i += 1
                    if not test:
                        self.insertNotFull(node.children[i], key, source, target, False)


    #TODO implement deleting key
    def deleteKey(key):
        null

    # search key in node
    # go through node and check if key is there
    # if not and node has no children -> key is not in the tree
    # if node has children go to child node with current index i
    def searchKey(self, key, nextNode = None):
        i = 0
        # go through node and check at which point key is smaller
        while i < len(nextNode.keys) and key > nextNode.keys[i]: 
            i += 1
        if i < len(nextNode.keys) and key == nextNode.keys[i]:
            return nextNode
        # if keys is not found and node is a leaf -> key is not in the tree
        elif nextNode.leaf: 
            return 'not in tree'
        #go to node in which key maybe is 
        return self.searchKey(key, nextNode.children[i]) 


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
        # empty list for edge conncection
        res = []
        edgeList = []
        # Base Case
        if node is None:
            return
        # Create an empty queue
        # for level order traversal
        queue = []
        # Enqueue Root and initialize height
        queue.append(node)
        while(len(queue) > 0):
            currNode = queue.pop(0)
            # Enqueue children
            for child in currNode.children:
                res.append(child.id)
                queue.append(child)
            edgeList.append(res.copy())
            res = []
        # frontend needs the edge list is in reverse level order, so just reverse the list
        edgeList.reverse()
        edgeListCopy = edgeList[:]
        self.edgeList = edgeListCopy

