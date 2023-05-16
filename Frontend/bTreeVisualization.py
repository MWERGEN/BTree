#   Created for BTree-MTT on 10.04.23
#
#   Creator: Tim Steiner
#
#   Tasks:  MBT-6
#
#   Editors:
#       1.      Tim Steiner on 10.04.23
#       2.      Marius Wergen on 27.04.23
#       3.      Marius Wergen on 02.05.23
#       4.      Marius Wergen on 03.05.23
#       5.      Marius Wergen on 04.05.23
#       6.      Marius Wergen on 07.05.23 
#       7.      Marius Wergen on 08.05.23
#       8.      Marius Wergen on 10.05.23
#       9.      Marius Wergen on 11.05.23
#       10.     Marius Wergen on 12.05.23
#       11.     Marius Wergen on 13.05.23
#       12.     Marius Wergen on 14.05.23
#
###############################################
#
#   File description:
#       - visualization of the B-tree
#

import time
import numpy as np
import math
import tkinter as Tk
from tkinter import ttk
import igraph as ig
import itertools as it
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler

from Frontend import anim as ani
from Backend import data

#root = tkinter.Tk()
#root.wm_title("Embedding in Tk")

# initialize the subplots where the graph will be displayed
# black background for design
##fig = plt.Figure()
##ax = fig.add_subplot(facecolor='black')

##root = Tk.Tk()
##root.geometry("700x400")

##label = Tk.Label(root,text="B-Tree control elements").grid(column=0, row=0)

##def test_button_clicked():
##    animTypeList = [1, 1, 1, 1, 0]
##    treeList = [[[5, 1], [[1, 2], [4, 5, 6], [8, 10, 15, 20], [40, 50, 60, 700], [100, 200, 420], [3, 7, 30, 80]], [[], [], [], [], [], [0, 1, 2, 3, 4]]], [[5, 1], [[1, 2], [4, 5, 6], [8, 10, 15, 20], [40, 50, 60, 700], [100, 200, 420], [3, 7, 30, 80]], [[], [], [], [], [], [0, 1, 2, 3, 4]]], [[5, 1], [[1, 2], [4, 5, 6], [8, 10, 17, 20], [40, 50, 60, 700], [100, 200, 420], [3, 7, 30, 80]], [[], [], [], [], [], [0, 1, 2, 3, 4]]], [[5, 1, 1], [[1, 2], [4, 5, 6], [8, 10, 17, 20], [40, 50, 60, 700], [100, 200, 420], [3, 7, 30, 80], []], [[], [], [], [], [], [0, 1, 2, 3, 4], []]], [[6, 2, 1], [[1, 2], [4, 5, 6], [8, 10], [17, 20], [40, 50, 60, 70], [100, 200, 420], [3, 7], [30, 80], [15]], [[], [], [], [], [], [], [0, 1, 2], [3, 4, 5], [6, 7]]]]
##    operands = [[5, 5, 2, 5, 6], [5, 2, 5, 6, 6], [0, 2, 3, 2, 0], [17, 17, 15, 15, 15]]

##button = Tk.Button(root, text='test', command=test_button_clicked)
##button.grid(column=0, row=1)

##label = Tk.Label(root,text="B-Tree visualization").grid(column=0, row=2)

##canvas = FigureCanvasTkAgg(fig, master=root)
##canvas.get_tk_widget().grid(column=0,row=3, sticky='nsew')
##root.columnconfigure(0, weight=1)
##root.rowconfigure(3, weight=1)

# Define a function to handle the resize event
##def on_resize(event):
##    """Resize the Matplotlib figure to match the tkinter canvas size"""
##    width = event.width
##    height = event.height
##    canvas.figure.set_size_inches(width/100, height/100)
##    canvas.draw()

# Bind the resize event to the tkinter window
##root.bind('<Configure>', on_resize)

# configuration for subplot area in matplotlib-window:
#   -   left, bottom, right, top define where the edge of the subplot area is on the matplotlib-window
#           -> by this configuration, the graph is positioned on the border of the window
#           -> depending on its width to height ratio, the part of the window where no graph is plotted is drawn white
#              whereas the part of the window where the graph is plotted has a gray background
#   -   wspace, hspace define the space between multiple subplots
#           -> we just have one subplot so these values are irrelevant  
##fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

#canvas = FigureCanvasTkAgg(fig, master=root)
#canvas.draw()

#toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
#toolbar.update()

#canvas.mpl_connect(
#    "key_press_event", lambda event: print(f"you pressed {event.key}"))
#canvas.mpl_connect("key_press_event", key_press_handler)

# button = tkinter.Button(master=root, text="Quit", command=root.quit)
# button.pack(side=tkinter.BOTTOM)

# toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
#canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

class BTreeVisualization:

    # constructor
    def __init__(self, k, keyWidth, refWidth, minNodeDistance, currentAnimation):
        # save passed animation for current animation
        self.currentAnimation = currentAnimation
        # save list of how many nodes are on each level of the tree
        self.nodesList = self.currentAnimation.nodesList
        # save list of which keys are in which node
        self.keysList = self.currentAnimation.keysList
        # safe edges in a List
        # format:       [[],     [],     [0, 1], ...]
        #   node         0       1         2
        #   edge to    none    none     node 0 and 1
        self.edgesList = self.currentAnimation.edgesList
        # list containing all edges as tupels
        self.edgesListTupel = []
        # generate a List with all Labels (key-Values)
        # -> chaining all elements in the lists in keysList together
        self.keyLabels = list(it.chain.from_iterable(self.keysList))
        # formatted keys (bold)
        self.keyLabelsFormatted = []
        # make labels bold
        self.formatLabels()
        # calculate how many nodes the Graph has
        self.numOfNodes = self.calcNumOfNodes(self.nodesList)
        # calculate how many keys the Graph has
        self.numOfKeys = self.calcNumOfKeys(self.keysList)
        # graph with Nodes (later surrounding keys and references of each node)
        self.gNodes = ig.Graph(self.numOfNodes)
        # graph with references inside the nodes
        self.gRefs = ig.Graph((2 * k + 1) * self.numOfNodes)
        # graph with aid-structure for reference-edge-visualization
        self.gRefsAid = ig.Graph((2 * k + 1) * self.numOfNodes)
        # graph with keys inside the nodes
        self.gKeys = ig.Graph(self.numOfKeys)
        # key for moving animation
        self.gMovingKey = ig.Graph(1)
        # x-Positions of Nodes' centers
        self.xGNodes = []
        # y-Positions of Nodes' centers
        self.yGNodes = []
        # x-Positions of references
        self.xGRefs = []
        # y-Positions of references
        self.yGRefs = []
        # x-Positions of aid-structures for refs
        self.xGRefsAid = []
        # y-Positions of aid-structures for refs
        self.yGRefsAid = []
        # x-Positions of keys
        self.xGKeys = []
        # y-Positions of keys
        self.yGKeys = []
        # x-Positions of moving keys
        self.xGMovingKey = []
        # y-Positions of moving keys
        self.yGMovingKey = []
        # tree's definition of k (= minimum number of keys in node)
        self.k = k
        # key-width
        self.keyWidth = keyWidth
        # ref-width
        self.refWidth = refWidth
        # node width
        #   = (2k keys + 2k references + outer right reference)
        #   = (2k * (keyWidth + refWidth)) + refWidth
        self.nodeWidth = self.k * 2 * (self.keyWidth + self.refWidth) + self.refWidth
        # horizontal distance between the tree's leafs
        # -> distances between other nodes are higher
        self.minNodeDistance = minNodeDistance
        # list containing the colors of each key
        self.colorKeyList = []
        # list containing the colors of each reference
        self.colorRefList = []
        # declare visual style
        self.visual_style = {}
        # rectangular vertices
        self.visual_style['vertex_shape'] = 'rectangle'
        #######
        # TK 
        #######
        
        self.fig = plt.Figure()
        # configuration for subplot area in matplotlib-window:
        #   -   left, bottom, right, top define where the edge of the subplot area is on the matplotlib-window
        #           -> by this configuration, the graph is positioned on the border of the window
        #           -> depending on its width to height ratio, the part of the window where no graph is plotted is drawn white
        #              whereas the part of the window where the graph is plotted has a gray background
        #   -   wspace, hspace define the space between multiple subplots
        #           -> we just have one subplot so these values are irrelevant  
        self.fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
        # initialize the subplots where the graph will be displayed
        # black background for design
        self.ax = self.fig.add_subplot(facecolor='black')
        self.root = Tk.Tk()
        # initialize the counter
        self.root.counter = 0
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.speed = 1
        self.scale = 0
        self.temp = 0
        self.backend = data.Backend(2)

    def countNext10Milliseconds(self):
        # check if 10 seconds have passed
        ##if self.root.counter == 10:
        ##    self.root.counter = 0
        ##    print("Called every 10 seconds")
        # increment the counter
        self.root.counter += 1
        # schedule the next call to my_function in 1 second
        self.root.after(10, self.countNext10Milliseconds)

    def initializeTK(self):
        # schedule the first call to my_function in 1 second
        self.root.after(10, self.countNext10Milliseconds)
        #self.root.geometry("700x400")

        label = Tk.Label(self.root,text="B-Tree control elements").grid(column=0, row=0)

        button0 = Tk.Button(self.root, text='insert 1 2 3 4 5', command=self.insert12345_button_clicked)
        button0.grid(column=0, row=1)

        button1 = Tk.Button(self.root, text='search 5', command=self.search_button_clicked)
        button1.grid(column=0, row=2)

        button2 = Tk.Button(self.root, text='insert 17', command=self.insert17_button_clicked)
        button2.grid(column=0, row=3)

        button2 = Tk.Button(self.root, text='insert 65', command=self.insert65_button_clicked)
        button2.grid(column=0, row=4)

        button3 = Tk.Button(self.root, text='delete 2 pt.1', command=self.delete_button_clicked)
        button3.grid(column=0, row=5)

        button4 = Tk.Button(self.root, text='delete 2 pt.2', command=self.delete2_button_clicked)
        button4.grid(column=0, row=6)

        # create a scale widget for selecting the number
        self.scale = Tk.Scale(self.root, from_=1, to=10, orient=Tk.HORIZONTAL)
        self.scale.grid(column=0, row=7)

        label = Tk.Label(self.root,text="B-Tree visualization").grid(column=0, row=8)
        
        self.canvas.get_tk_widget().grid(column=0,row=9, sticky='nsew')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(9, weight=1)

        # Create a frame inside the canvas to hold the content
        #frame = ttk.Frame(self.canvas)
        #self.canvas.create_window(0, 0, anchor='nw', window=frame)

        # Create a scrollbar
        scrollbar = ttk.Scrollbar(self.root, orient=Tk.VERTICAL, command=self.canvas.get_tk_widget().yview)
        scrollbar.grid(row=9, column=1, sticky="ns")
        self.canvas.get_tk_widget().configure(yscrollcommand=scrollbar.set)

        self.root.bind("<Configure>", self.update_scroll_region)
        # Bind the resize event to the tkinter window

    def insert17_button_clicked(self):
        # self.currentAnimation = self.backendObj.insert(17)

        # die erstellst du
        animTypeList = [1, 1, 1, 1, 0]
        # für jeden Eintrag in animTypeList ein Baum
        # heißt:    len(animTypeList) = len(treeList)
        #           -- ein Baum ----------------------------------------------------------------------------------------------------------------------------
        #            -NpL-   - Keys per Level (KpL)-----------------------------------------------------------------   - edgeList ------------------------  
        treeList = [[[5, 1], [[1, 2], [4, 5, 6], [8, 10, 15, 20], [40, 50, 60, 700], [100, 200, 420], [3, 7, 30, 80]], [[], [], [], [], [], [0, 1, 2, 3, 4]]], [[5, 1], [[1, 2], [4, 5, 6], [8, 10, 15, 20], [40, 50, 60, 700], [100, 200, 420], [3, 7, 30, 80]], [[], [], [], [], [], [0, 1, 2, 3, 4]]], [[5, 1], [[1, 2], [4, 5, 6], [8, 10, 17, 20], [40, 50, 60, 700], [100, 200, 420], [3, 7, 30, 80]], [[], [], [], [], [], [0, 1, 2, 3, 4]]], [[5, 1, 1], [[1, 2], [4, 5, 6], [8, 10, 17, 20], [40, 50, 60, 700], [100, 200, 420], [3, 7, 30, 80], []], [[], [], [], [], [], [0, 1, 2, 3, 4], []]], [[6, 2, 1], [[1, 2], [4, 5, 6], [8, 10], [17, 20], [40, 50, 60, 70], [100, 200, 420], [3, 7], [30, 80], [15]], [[], [], [], [], [], [], [0, 1, 2], [3, 4, 5], [6, 7]]]]
        #           -- source ----   ---- target --   -- refs * ----   -- labels ---------
        operands = [[5, 5, 2, 5, 6], [5, 2, 5, 6, 6], [0, 2, 3, 2, 0], [17, 17, 15, 15, 15]]
        # * zu den references:  wenn Knoten runter geht:    Referenz des Startknotens auf Zielknoten (wievielter)
        #                       wenn Knoten hoch geht:      einfach 0
        #                       wenn Type = 0:              einfach 0
        # bis hier
                                # das hier würde ich zurück bekommen
        self.currentAnimation = ani.Animation(animTypeList, treeList, operands)

    def insert12345_button_clicked(self):
        self.temp += 1
        if self.temp == 1:
            #animTypeList = [1, 0]
            #treeList = [[[1], [[]], [[]]], [[1], [[1]], [[]]]]
            #operands = [[0, 0], [0, 0], [0, 0], [1, 1]]
            self.backend.insertKeyIntoTree(1)
            animationList = self.backend.animationList
            treeList = self.backend.treeList
            operands = self.backend.operands
        elif self.temp == 2:
            #animTypeList = [1, 0]
            #treeList = [[[1], [[1]], [[]]], [[1], [[1, 2]], [[]]]]
            #operands = [[0, 0], [0, 0], [0, 0], [2, 2]]
            self.backend.insertKeyIntoTree(9999)
            animationList = self.backend.animationList
            treeList = self.backend.treeList
            operands = self.backend.operands
        elif self.temp == 3:
            #animTypeList = [1, 0]
            #treeList = [[[1], [[1, 2]], [[]]], [[1], [[1, 2, 3]], [[]]]]
            #operands = [[0, 0], [0, 0], [0, 0], [3, 3]]
            self.backend.insertKeyIntoTree(3)
            animationList = self.backend.animationList
            treeList = self.backend.treeList
            operands = self.backend.operands
        elif self.temp == 4:
            #animTypeList = [1, 0]
            #treeList = [[[1], [[1, 2, 3]], [[]]], [[1], [[1, 2, 3, 4]], [[]]]]
            #operands = [[0, 0], [0, 0], [0, 0], [4, 4]]
            self.backend.insertKeyIntoTree(4)
            animationList = self.backend.animationList
            treeList = self.backend.treeList
            operands = self.backend.operands
        elif self.temp == 5:
            #animTypeList = [1, 1, 0]
            #treeList = [[[1], [[1, 2, 3, 4]], [[]]], [[1, 1], [[1, 2, 3, 4], []], [[], []]], [[2, 1], [[1, 2], [4, 5], [3]], [[], [], [0, 1]]]]
            #operands = [[0, 0, 0], [0, 1, 0], [0, 0, 0], [5, 3, 3]]
            self.backend.insertKeyIntoTree(5)
            animationList = self.backend.animationList
            treeList = self.backend.treeList
            operands = self.backend.operands
        elif self.temp == 6:
            #animTypeList = [1, 1, 0]
            #treeList = [[[1], [[1, 2, 3, 4]], [[]]], [[1, 1], [[1, 2, 3, 4], []], [[], []]], [[2, 1], [[1, 2], [4, 5], [3]], [[], [], [0, 1]]]]
            #operands = [[0, 0, 0], [0, 1, 0], [0, 0, 0], [5, 3, 3]]
            self.backend.insertKeyIntoTree(6)
            animationList = self.backend.animationList
            treeList = self.backend.treeList
            operands = self.backend.operands
        elif self.temp == 7:
            #animTypeList = [1, 1, 0]
            #treeList = [[[1], [[1, 2, 3, 4]], [[]]], [[1, 1], [[1, 2, 3, 4], []], [[], []]], [[2, 1], [[1, 2], [4, 5], [3]], [[], [], [0, 1]]]]
            #operands = [[0, 0, 0], [0, 1, 0], [0, 0, 0], [5, 3, 3]]
            self.backend.insertKeyIntoTree(7)
            animationList = self.backend.animationList
            treeList = self.backend.treeList
            operands = self.backend.operands
        elif self.temp == 8:
            animationList = [1, 1, 1, 0]
            treeList = [[[2, 1], [[1, 2], [4, 5, 6, 7], [3]], [[], [], [0, 1]]], [[2, 1], [[1, 2], [4, 5, 6, 7], [3]], [[], [], [0, 1]]], [[2, 1], [[1, 2], [4, 5, 7, 8], [3]], [[], [], [0, 1]]], [[3, 1], [[1, 2], [4, 5], [7, 8], [3, 6]], [[], [], [], [0, 1, 2]]]]
            operands = [[2, 2, 1, 2], [2, 1, 2, 2], [0, 1, 4, 1], [8, 8, 6, 6]]
        else:
            animationList = [0]
            treeList = [[[1], [[]], [[], [], []]]]
            operands = []

        print(animationList)
        print(treeList)
        print(operands)
        self.currentAnimation = ani.Animation(animationList, treeList, operands)

    def insert65_button_clicked(self):
        # self.currentAnimation = self.backendObj.insert(17)

        # die erstellst du
        animTypeList = [1, 1, 1, 1, 0]
        # für jeden Eintrag in animTypeList ein Baum
        # heißt:    len(animTypeList) = len(treeList)
        #           -- ein Baum ----------------------------------------------------------------------------------------------------------------------------
        #            -NpL-   - Keys per Level (KpL)-----------------------------------------------------------------   - edgeList ------------------------  
        treeList = [[[5, 1], [[1, 2], [4, 5, 6], [8, 10, 15, 20], [40, 50, 60, 700], [100, 200, 420], [3, 7, 30, 80]], [[], [], [], [], [], [0, 1, 2, 3, 4]]], [[5, 1], [[1, 2], [4, 5, 6], [8, 10, 15, 20], [40, 50, 60, 700], [100, 200, 420], [3, 7, 30, 80]], [[], [], [], [], [], [0, 1, 2, 3, 4]]], [[5, 1], [[1, 2], [4, 5, 6], [8, 10, 15, 20], [40, 50, 65, 700], [100, 200, 420], [3, 7, 30, 80]], [[], [], [], [], [], [0, 1, 2, 3, 4]]], [[5, 1, 1], [[1, 2], [4, 5, 6], [8, 10, 15, 20], [40, 50, 60, 700], [100, 200, 420], [3, 7, 60, 80], []], [[], [], [], [], [], [0, 1, 2, 3, 4], []]], [[6, 2, 1], [[1, 2], [4, 5, 6], [8, 10, 15, 20], [40, 50], [65, 70], [100, 200, 420], [3, 7], [60, 80], [30]], [[], [], [], [], [], [], [0, 1, 2], [3, 4, 5], [6, 7]]]]
        #           -- source ----   ---- target --   -- refs * ----   -- labels ---------
        operands = [[5, 5, 3, 5, 6], [5, 3, 5, 6, 6], [0, 3, 0, 0, 0], [65, 65, 60, 30, 30]]
        # * zu den references:  wenn Knoten runter geht:    Referenz des Startknotens auf Zielknoten (wievielter)
        #                       wenn Knoten hoch geht:      einfach 0
        #                       wenn Type = 0:              einfach 0
        # bis hier
                                # das hier würde ich zurück bekommen
        self.currentAnimation = ani.Animation(animTypeList, treeList, operands)

    def search_button_clicked(self):
        # type 2 heißt suchen (bzw. löschen)
        animTypeList = [2, 0]
        # zwei Bäume, da zwei Animationen
        treeList = [[[5, 1], [[1, 2], [4, 5, 6], [9, 10, 15, 20], [40, 50, 60, 700], [100, 200, 420], [3, 7, 30, 80]], [[], [], [], [], [], [0, 1, 2, 3, 4]]], [[5, 1], [[1, 2], [4, 5, 6], [9, 10, 15, 20], [40, 50, 60, 700], [100, 200, 420], [3, 7, 30, 80]], [[], [], [], [], [], [0, 1, 2, 3, 4]]]]
        #           1.   2.      3.
        # 1.:   welchen Key suchen wir?
        # 2.:   welche Knoten haben wir abgesucht?
        # 3.:   Key gefunden?
        operands = [5, [5, 1], True]
        self.currentAnimation = ani.Animation(animTypeList, treeList, operands)

    def delete_button_clicked(self):
        animTypeList = [2, 0]
        treeList = [[[5, 1], [[1, 2], [4, 5, 6], [9, 10, 15, 20], [40, 50, 60, 700], [100, 200, 420], [3, 7, 30, 80]], [[], [], [], [], [], [0, 1, 2, 3, 4]]], [[5, 1], [[1], [4, 5, 6], [9, 10, 15, 20], [40, 50, 60, 700], [100, 200, 420], [3, 7, 30, 80]], [[], [], [], [], [], [0, 1, 2, 3, 4]]]]
        operands = [2, [5, 0], True]
        self.currentAnimation = ani.Animation(animTypeList, treeList, operands)

    def delete2_button_clicked(self):
        animTypeList = [1, 1, 0]
        treeList = [[[5, 1], [[1], [5, 6], [9, 10, 15, 20], [40, 50, 60, 700], [100, 200, 420], [3, 7, 30, 80]], [[], [], [], [], [], [0, 1, 2, 3, 4]]], [[5, 1], [[1], [5, 6], [9, 10, 15, 20], [40, 50, 60, 700], [100, 200, 420], [4, 7, 30, 80]], [[], [], [], [], [], [0, 1, 2, 3, 4]]], [[5, 1], [[1, 3], [5, 6], [9, 10, 15, 20], [40, 50, 60, 700], [100, 200, 420], [4, 7, 30, 80]], [[], [], [], [], [], [0, 1, 2, 3, 4]]]] 
        operands = [[1, 5, 0], [5, 0, 0], [0, 0, 0], [4, 3, 3]]
        self.currentAnimation = ani.Animation(animTypeList, treeList, operands)

    def get_row_height(self, widget, row):
        # Get the number of rows and columns in the grid
        num_rows = widget.grid_size()[1]
        # Check if the specified row is within the valid range
        if row >= num_rows:
            raise IndexError("Row index out of range")
        # Get the bounding box information of the specified row
        bbox = widget.grid_bbox(row, 0)
        # Calculate the height of the row
        height = bbox[3] - bbox[1]
        return height

    # Update the scrollable region when the canvas size changes
    def update_scroll_region(self, event):
        self.canvas.get_tk_widget().configure(scrollregion=self.canvas.get_tk_widget().bbox("all"))

    # resets all values of the graph in order to print it again in a different form
    def updateGraph(self):
        # graph's nodes
        self.nodesList = self.currentAnimation.nodesList
        # graph's keys
        self.keysList = self.currentAnimation.keysList
        # graph's edges
        self.edgesList = self.currentAnimation.edgesList
        # list containing all edges as tupels
        self.edgesListTupel = []
        # generate a List with all Labels (key-Values)
        # -> chaining all elements in the lists in keysList together
        self.keyLabels = list(it.chain.from_iterable(self.keysList))
        # formatted keys (bold)
        self.keyLabelsFormatted = []
        # make labels bold
        self.formatLabels()
        # calculate how many nodes the Graph has
        self.numOfNodes = self.calcNumOfNodes(self.nodesList)
        # calculate how many keys the Graph has
        self.numOfKeys = self.calcNumOfKeys(self.keysList)
        # graph with Nodes (later surrounding keys and references of each node)
        self.gNodes = ig.Graph(self.numOfNodes)
        # graph with references inside the nodes
        self.gRefs = ig.Graph((2 * self.k + 1) * self.numOfNodes)
        # graph with aid-structure for reference-edge-visualization
        self.gRefsAid = ig.Graph((2 * self.k + 1) * self.numOfNodes)
        # graph with keys inside the nodes
        self.gKeys = ig.Graph(self.numOfKeys)
        # key for moving animation
        #self.gMovingKey = ig.Graph(1)
        # x-Positions of Nodes' centers
        self.xGNodes = []
        # y-Positions of Nodes' centers
        self.yGNodes = []
        # x-Positions of references
        self.xGRefs = []
        # y-Positions of references
        self.yGRefs = []
        # x-Positions of aid-structures for refs
        self.xGRefsAid = []
        # y-Positions of aid-structures for refs
        self.yGRefsAid = []
        # x-Positions of keys
        self.xGKeys = []
        # y-Positions of keys
        self.yGKeys = []
        # list containing the colors of each key
        self.colorKeyList = []
        # list containing the colors of each reference
        self.colorRefList = []
        # predefine nodes
        self.calcNodesPositions()
        # calc where the references will be inside the nodes
        self.calcRefPositions()
        # calc where the keys will be inside the nodes
        self.calcKeyPositions()
        # calculate all graphs
        self.assertValuesToGraphs()
        # calculate the edges' relationships
        self.calcEdges()

    # initializes all keys with a lightblue background
    def initializeColorKeyList(self):
        self.colorKeyList = []
        # for n keys, we need a list with n times the color
        for i in self.xGKeys:
            # add another instance of the lightblue
            self.colorKeyList.append("lightblue")

    # initializes all refs with a gray background
    def initializeColorRefList(self):
        self.colorRefList = []
        # for n refs, we need a list with n times the color
        for i in self.xGRefs:
            # add another instance of the gray
            self.colorRefList.append("gray")

    # takes all labels and makes them bold
    def formatLabels(self):
        self.keyLabelsFormatted = []
        # iterate over all labels
        for i in self.keyLabels:
            # format each Label with a LaTex expression
            # expression makes the label bold
            self.keyLabelsFormatted.append('$\\mathbf{' + str(i) + '}$')

    # calculates how many nodes the nodesList has combined
    def calcNumOfNodes(self, nodesList):
        # counts number of nodes
        nodeCtr = 0
        # iterates over nodesList
        for i in nodesList:
            # nodesList's elements are the number of nodes on a specific level = i
            # so we count the numbers of nodes on each level together
            nodeCtr += i
        # return total number of nodes in nodesList
        return nodeCtr
    
    # calculates how many keys the keysList has combined
    def calcNumOfKeys(self, keysList):
        # counts number of keys
        keyCtr = 0
        # iterates over keysList
        for i in keysList:
            # add the number of keys in every node to the counter
            keyCtr += len(i)
        # return total number of keys
        return keyCtr

    # calc the x and y positions of all nodes
    # we start on the lowest level (leafs) and work upwards
    # and work from left to right for each level
    def calcNodesPositions(self):
        # counter for tree level
        # lower level (leafs) = level 1
        ctrLevel = 1
        # iterate over nodesList
        for i in self.nodesList:
            # number of nodes on level is equal
            if (i % 2 == 0):
                # counter for node position on level
                # example: 4 nodes on a level
                #   nodes:  |node1|   |node2|   |node3|   |node4|
                #   ------------------------------------------------
                #   ctrEven   -3        -1         1         3 
                ctrEven = (-1) * (i - 1)
                # calculate all nodes' positions
                # in our example: -3, -1, 1, 3(= 4-1)
                while ctrEven <= (i - 1):
                    # save x-Position 
                    # fixed point for calculation is (0,0)
                    # the distance from (0,0) to the node rigth/left from the centre is
                    # half the width of a node + half the distance between two nodes
                    # let's call this distance d
                    # the distance to the next node from there on is 2 * d (-> thats why we raise ctrEven later by two)
                    # multiplication with ctrLevel is for dynamic distance
                    # -> the higher the level, the more distance is needed
                    self.xGNodes.append(0.5 * ctrLevel * (self.nodeWidth + self.minNodeDistance) * ctrEven)
                    # save same y-Position for all nodes on one level
                    self.yGNodes.append(ctrLevel)
                    # distance to next node is 2 * d (watch above)
                    ctrEven += 2
            # number of nodes on level is NOT equal
            else:
                # counter for node position on level
                # example: 5 nodes on a level
                #   nodes:  |node1|   |node2|   |node3|   |node4|   |node5|
                #   ---------------------------------------------------------
                #   ctrOdd   -2        -1         0         2         3
                ctrOdd = (i - 1) * (-0.5)
                # calculate all nodes' positions
                # indeces in our example: -2, -1, 0, 1, 2(= (5-1)*1/2 )
                while ctrOdd <= (i - 1) * (0.5):
                    # save x-Position 
                    # fixed point for calculation is (0,0)
                    # the distance from (0,0) to the node rigth/left from the centre is
                    # the width of a node + the distance between two nodes
                    # let's call this distance d
                    # the distance to the next node from there on is d (-> thats why we raise ctrEven later by one)
                    # multiplication with ctrLevel is for dynamic distance
                    # -> the higher the level, the more distance is needed
                    self.xGNodes.append(ctrLevel * (self.nodeWidth + self.minNodeDistance) * ctrOdd)
                    # save same y-Position for all nodes on one level
                    self.yGNodes.append(ctrLevel)
                    # distance to next node is d (watch above)
                    ctrOdd += 1
            # the next element in nodesList describes the number of nodes on the upper level
            # -> so the level has to be incremented
            ctrLevel += 1

    # calculates the x and y positions of all references
    def calcRefPositions(self):
        # iterate over all nodes' x positions 
        for i in self.xGNodes:
            # initialize a counter starting at -k
            ctr = (-1) * self.k
            # each node has 2k + 1 references (-k to k including 0)
            while ctr <= self.k:
                # each ref has a predefined widht (self.keyWidth)
                # adding k refs left from centre of node when i is negative
                # adding k refs right from centre of node when i is positive
                # adding 1 ref in the middle of the node
                self.xGRefs.append(i + ((self.refWidth + self.keyWidth) * ctr))
                # edges should stick on the center x-Pos of a reference
                self.xGRefsAid.append(i + ((self.refWidth + self.keyWidth) * ctr))
                # increment counter each iteration
                ctr += 1
        # iterate over all nodes' y positions
        for j in self.yGNodes:
            # initialize counter starting at 0
            ctr2 = 0
            # each node has 2k + 1 references (0 to 2k)
            while ctr2 <= 2 * self.k:
                # y position of each ref inside a specific node is equal to nodes y position
                self.yGRefs.append(j)
                # y position is the bottom of the ref in order to force the edges to stick at the bottom of a ref
                self.yGRefsAid.append(j - 2 * self.refWidth)
                # increment counter
                ctr2 += 1

    # calculates the x and y positions of all keys
    def calcKeyPositions(self):
        # counter which node is currently touched
        ctrNodes = 0
        # iterate over all nodes' x positions 
        for i in self.xGNodes:
            # the left outer key in a node is:
            #   ->  the centre of the node (i)
            #           minus (k - 1) key- and refWidths
            #           minus 0.5 key- and refWidths
            # this temp-variable will be raised by (keyWidth + refWidth) for the next key in the node
            nextKeyXPosition = i - (self.k - 0.5) * (self.keyWidth + self.refWidth)
            # iterate over all keys in the current node
            for j in self.keysList[ctrNodes]:
                # add the calculates x-Position for the key to the key-graph-list
                self.xGKeys.append(nextKeyXPosition)
                # the next key is one key-width and one ref-width right from the current x-position
                nextKeyXPosition += (self.keyWidth + self.refWidth)
            # increment node-counter because the next iteration of the for loop will be for the next node
            ctrNodes += 1
        # reset Node counter for the y-Positions
        ctrNodes = 0
        # iterate over all nodes' y positions
        for k in self.yGNodes:
            # add as many y positions as there are keys in one node
            for l in self.keysList[ctrNodes]:
                # y position of each key inside a specific node is equal to nodes y position
                self.yGKeys.append(k)
            # increment node-counter because the next iteration of the for loop will be for the next node
            ctrNodes += 1
    
    # calculates the ref to ref connection for all edges
    def calcEdges(self):
        # counter which node is worked on
        ctrNode = 0
        # iterate over all edges
        for i in self.edgesList:
            # only conside lists in edgesList that are not empty
            # empty list in edgesList means no edges for this node
            if i:
                # counter which ref inside the node is worked on
                ctrRef = 0
                # iterate over all edges for the considered node
                for j in i:
                    # calculate parent ref
                    #   the outer left reference in the bottom left node is ref 0
                    #       now we have to calculate which index the outer left reference in our node has
                    #       we are in node ctrNode with 2 * k + 1 refs per node
                    #       so the index of the outer left ref is: ctrNode * (2 * k + 1)
                    #   we have to add ctrRef to aim a specific reference in the node
                    parent = ctrNode * (2 * self.k + 1) + ctrRef
                    # calculate child ref
                    #   the outer left reference in the bottom left node is ref 0
                    #       now we have to calculate which index the outer left reference in the child node has
                    #       the child node has index j with 2 * k + 1 refs per node
                    #       so the index of the outer left ref is: j * (2 * k + 1)
                    #   we have to add k to aim the center reference in the child-node
                    child = j * (2 * self.k + 1) + self.k
                    # add edge = (parentRef, childRef) to edgesListTupel
                    self.edgesListTupel.append((parent, child))
                    # increment ctrRef to aim for the right next ref in the node for the following iteration
                    ctrRef += 1
            # increment ctrNode to observe the next node in the next iteration
            ctrNode += 1
        # after calculating all edges' relationships, 
        # add the edges to the graph of the references Aid structures
        self.gRefsAid.add_edges(self.edgesListTupel)

    # define the x- and y-Positions and potential labels for all Graphs
    def assertValuesToGraphs(self):
        # for Nodes x
        self.gNodes.vs['x'] = self.xGNodes
        # for Nodes y
        self.gNodes.vs['y'] = self.yGNodes
        # for Refs x
        self.gRefs.vs['x'] = self.xGRefs
        # for Refs y
        self.gRefs.vs['y'] = self.yGRefs
        # for aid x
        self.gRefsAid.vs['x'] = self.xGRefsAid
        # for aid y
        self.gRefsAid.vs['y'] = self.yGRefsAid
        # for Keys x
        self.gKeys.vs['x'] = self.xGKeys
        # for Keys y
        self.gKeys.vs['y'] = self.yGKeys
        # assert the labels (key-values) to the key-graph
        self.gKeys.vs['label'] = self.keyLabelsFormatted
        # generate a list with the colors for each node
        self.initializeColorKeyList()
        # generate a list with the colors for each ref
        self.initializeColorRefList()

    # animation of type 1
    # moves a new key from one node to another
    # width and height are w and h from the subplot
    # -> used for custom font size
    def animation1(self, width, height):
        # save current animation in temp anim
        # used for better overview in complex code
        anim = self.currentAnimation
        # reset the root counter for time scheduling
        if not anim.resetted:
            # reset counter
            self.root.counter = 0
            # prevent counter to be resetted every iteration
            anim.resetted = True
            anim.updateNewAnimation()                                   ### !!!!!!!!!!!!!!!!!!!!
            self.updateGraph()
        # if the starting node is lower than the destination node
        # -> means that the key should move upwards
        if (anim.startingNode[anim.walkthrough] < anim.destinationNode[anim.walkthrough]):
            anim.upwards = True
        else:
            anim.upwards = False
        
        # moving node is going up
        if anim.upwards:
            if anim.walkthrough == 0:
                anim.startingRefX = self.xGRefsAid[anim.startingNode[anim.walkthrough] * (2 * self.k + 1) + self.k]
                anim.startingRefY = self.yGRefsAid[anim.startingNode[anim.walkthrough] * (2 * self.k + 1) + self.k] + 7 * self.refWidth
            else:
                # calculates the x-Position where the key starts
                # simply counts to the reference where the key starts and gets that x-value
                anim.startingRefX = anim.currX[0]
                # calculates the y-Position where the key starts
                # simply counts to the reference where the key starts and gets that y-value
                anim.startingRefY = anim.currY[0]
            # calculates the x-Position where the key has to end
            # simply counts to the center of the node where the key should end and gets that x-value
            anim.destinationRefX = self.xGRefsAid[anim.destinationNode[anim.walkthrough] * (2 * self.k + 1) + self.k]
            # calculates the y-Position where the key has to end
            # simply counts to the center of the node where the key should end and gets that y-value
            anim.destinationRefY = self.yGRefsAid[anim.destinationNode[anim.walkthrough] * (2 * self.k + 1) + self.k] + 7 * self.refWidth
        # moving node is going down
        else:
            # calculates the x-Position where the key starts
            # simply counts to the reference where the key starts and gets that x-value
            anim.startingRefX = self.xGRefsAid[anim.startingNode[anim.walkthrough] * (2 * self.k + 1) + anim.refInsideStartingNode[anim.walkthrough]]
            # calculates the y-Position where the key starts
            # simply counts to the reference where the key starts and gets that y-value
            anim.startingRefY = self.yGRefsAid[anim.startingNode[anim.walkthrough] * (2 * self.k + 1) + anim.refInsideStartingNode[anim.walkthrough]]
            # calculates the x-Position where the key has to end
            # simply counts to the center of the node where the key should end and gets that x-value
            anim.destinationRefX = self.xGRefsAid[anim.destinationNode[anim.walkthrough] * (2 * self.k + 1) + self.k]
            # calculates the y-Position where the key has to end
            # simply counts to the center of the node where the key should end and gets that y-value
            anim.destinationRefY = self.yGRefsAid[anim.destinationNode[anim.walkthrough] * (2 * self.k + 1) + self.k]
        # case differentiation to avoid deviding by zero
        if (anim.startingRefY - anim.destinationRefY) != 0:
            # calculate the gradient of the connecting edge between the startingNode and the destinationNode
            # gradient g is relative to y: g(y) = x
            #   -> the idea is that the moving node moves some pixels down and the corresponding pixels to the side
            #   -> so all keys move at the same speed no matter the edge
            anim.gradient = (anim.startingRefX - anim.destinationRefX) / (anim.startingRefY - anim.destinationRefY)
        # only for first iteration
        if anim.flagNoMove:
            # only initialize starting point in the first iteration
            # exceptional case for root
            if anim.startingNode[anim.walkthrough] == anim.destinationNode[anim.walkthrough]:
                # position moving node left beside the node: x-position
                anim.currX[0] = anim.startingRefX - (anim.refInsideStartingNode[anim.walkthrough] + 2) * (self.keyWidth)
                # position moving node left beside the node: x-position
                anim.currY[0] = anim.startingRefY + 2 * self.refWidth
            # for all other nodes
            elif not anim.upwards and anim.currY[0] != (anim.destinationRefY  + 7 * self.refWidth) or anim.upwards and anim.currY[0] != (anim.destinationRefY):
                # let the key begin at the starting point
                # x
                anim.currX[0] = anim.startingRefX
                # y
                anim.currY[0] = anim.startingRefY
                # start moving the key
                anim.flagNoMove = False
        # during the animation
        # -> repositioning the node
        else:
            # moving node is going upwards
            if anim.upwards:
                # if the key is not surpassing the destination node
                if anim.currY[0] + anim.animationSpeed < anim.destinationRefY:
                    # move one unit horizontally
                    anim.currX[0] += anim.animationSpeed * anim.gradient
                    # move one unit up
                    anim.currY[0] += anim.animationSpeed
                # if the key would surpass the destination node in the next iteration
                else:
                    # reset the counter if the comparison will start
                    self.root.counter = 0
                    # stop the key ahead of the destination node
                    # y position exactly on edge
                    anim.currY[0] = anim.destinationRefY
                    # x position in the middle of the node if destinationRefX == center of node
                    anim.currX[0] = anim.destinationRefX
                    # end of animation reached means stop animation
                    anim.flagNoMove = True
            else:
                # if the key is not surpassing the destination node
                if anim.currY[0] - anim.animationSpeed > anim.destinationRefY + 7 * self.refWidth:
                    # move one unit horizontally
                    anim.currX[0] -= anim.animationSpeed * anim.gradient
                    # move one unit down
                    anim.currY[0] -= anim.animationSpeed
                # if the key would surpass the destination node in the next iteration
                else:          
                    # reset the counter if the comparison will start
                    self.root.counter = 0     
                    # stop the key ahead of the destination node
                    # y position exactly on edge
                    anim.currY[0] = anim.destinationRefY + 7 * self.refWidth
                    # x position exactly on edge
                    anim.currX[0] = anim.startingRefX - (anim.startingRefY - anim.currY[0]) * anim.gradient
                    # end of animation reached means stop animation
                    anim.flagNoMove = True
        # assert x-Position of moving Node to moving-Node-Graph
        self.gMovingKey.vs['x'] = anim.currX
        # assert y-Position of moving Node to moving-Node-Graph
        self.gMovingKey.vs['y'] = anim.currY
        # assert label of moving Node to moving-Node-Graph
        self.gMovingKey.vs['label'] = anim.labelFormatted
        # check if the root is empty
        # its the case when there is a new root
        if len(anim.keysList[len(anim.keysList) - 1]) == 0:
            # skip the animation following
            anim.newRoot = True
            anim.flagOuterKeyReached = True
        # do the comparison animation if the moving key is ready 
        # and the comparison animation is not ready yet
        if not anim.flagOuterKeyReached and anim.flagNoMove and not anim.newRoot:
            # counter to find out which node has to be observed
            ctrNode = 0
            # index counts what's the index of the observed key inside the keys list
            index = 0
            # count the number of all keys together
            while ctrNode < anim.destinationNode[anim.walkthrough]:
                # add as many keys to index that are in the node at position ctrNode
                index += len(self.keysList[ctrNode])
                # next node
                ctrNode += 1
            # add to the index the rank of the ref inside the node
            index += anim.highlightedKey
            # paint the observed key red to indicate that it is being observed
            self.colorKeyList[index] = "red"
            # a key was found that is higher than the key that is going to be added
            if self.keyLabels[index] > anim.label:
                # stop the animation
                anim.flagOuterKeyReached = True
            # the key that is going to be added would be the highest key in the observed node
            elif anim.highlightedKey == len(self.keysList[ctrNode]) - 1:
                # stop the animation
                anim.flagOuterKeyReached = True
                # indicate that it would be the highest key inside the node
                anim.flagNewKeyHighest = True
            # observe one key all 50 to 500 milliseconds (depending on users selection)
            elif self.root.counter != 0 and self.root.counter % round(50 / self.speed) == 0:
                # after 30 frames, switch to the following key
                anim.highlightedKey += 1
        # make all keys lightblue again all 50 to 500 milliseconds (depending on users selection)
        if self.root.counter != 0 and self.root.counter % round(50 / self.speed) == 0:
            # reset counter for next part of animation
            #anim.resetted = False
            # set all keys to lightblue
            self.initializeColorKeyList()
            # if the comparison animation is over
            if anim.flagOuterKeyReached and anim.flagNoMove:
                # if there is still another part of the animation, trigger it
                if (anim.walkthrough + 1) < len(anim.destinationNode):
                    # switch to the next animation
                    anim.walkthrough += 1
                    # reset destination
                    #anim.destinationRefY = 0
                    # reset highlighted key
                    #anim.highlightedKey = 0
                    # reset flags to default
                    anim.flagOuterKeyReached = False
                    anim.flagNewKeyHighest = False
                    # updates label
                    # -> is needed for a moving node going up (maybe with a different label)
                    anim.label = anim.operands[3][anim.walkthrough]
                    # apply changes
                    anim.setLabel(anim.label)
                    anim.updateNewAnimation()
                    self.updateGraph()
                    # ref-coloring
                    # first check if the walkthrough is not the first one
                    # first one is root comparison
                    if anim.walkthrough < len(anim.startingNode) - 1:
                        # only color the ref green if the node is going down in the next part-animation
                        if (anim.startingNode[anim.walkthrough + 1] < anim.destinationNode[anim.walkthrough + 1]):
                            # if the key would be the highest in the node
                            if anim.flagNewKeyHighest:
                                # paint the outer right ref green 
                                # = the found path
                                self.colorRefList[anim.destinationNode[anim.walkthrough - 1] * (2 * self.k + 1) + anim.highlightedKey + 1] = "green"
                            # if the key is not the highest in the node
                            else:
                                # paint the ref left from the higher key green
                                # = the found path
                                self.colorRefList[anim.destinationNode[anim.walkthrough - 1] * (2 * self.k + 1) + anim.highlightedKey] = "green"
                    # reset highlighted key
                    anim.highlightedKey = 0        
                # wait a bit if there is no other animation left
                # so the key stays ahead of his new node
                # -> the user can observe the destination position 
                else:
                    # update the animation
                    # sets the new type
                    # -> so until a new animation comes in, just the graph is drawn
                    anim.updateNewAnimation()
                    # update the graph
                    # -> needed for new, inserted key
                    self.updateGraph()
                    self.initializeColorRefList()
        # only plot moving node if the animation is still chosen
        # this is needed because the animation type can be = 0 for one iteration
        # without the if, the moving node would be drawn anywhere, which looks buggy
        if anim.type == 1:
            # define plot for moving key
            ig.plot(
                # moving key graph
                self.gMovingKey,
                # targetted subplot
                target = self.ax,
                # width of key
                vertex_width = self.keyWidth,
                # choose height = width of 4 refs
                vertex_height = 4 * self.refWidth,
                # lightblue means key node
                vertex_color = "lightblue",
                # set color of moving vertex to red
                vertex_frame_color="red",
                # formula for dynamically resizing the labels, so they are perfectly fitting into the node
                # width and height depend on the axes of the graph
                vertex_label_size = 0.92 * math.sqrt(width) * math.sqrt(height),
                # append style
                **self.visual_style, 
            )

    # animation of type 2
    # searches a key
    # width and height are w and h from the subplot
    # -> used for custom font size
    def animation2(self):
        # save current animation in temp anim
        # used for better overview in complex code
        anim = self.currentAnimation
        # in the beginning (first iteration) of the animation:
        # reset the root counter for time scheduling
        if not anim.resetted:
            # reset counter
            self.root.counter = 0
            # prevent counter to be resetted every iteration
            anim.resetted = True
        # counter to find out which node has to be observed
        ctrNode = 0
        # index counts what's the index of the observed key inside the keys list
        index = 0
        # count the number of all keys together
        while ctrNode < anim.checkNodes[anim.walkthrough]:
            # add as many keys to index that are in the node at position ctrNode
            index += len(self.keysList[ctrNode])
            # next node
            ctrNode += 1
        # add to the index the rank of the ref inside the node
        index += anim.highlightedKey
        # paint the observed key red to indicate that it is being observed
        self.colorKeyList[index] = "red"
        # the searched key was found
        if self.keyLabels[index] == anim.searchKey:
            # mark the found key green
            self.colorKeyList[index] = "green"
            # stop the animation
            anim.flagOuterKeyReached = True
        # a key was found that is higher than the key that is going to be added
        elif self.keyLabels[index] > anim.searchKey:
            # stop the animation
            anim.flagOuterKeyReached = True
        # the key that is going to be added would be the highest key in the observed node
        elif anim.highlightedKey == len(self.keysList[ctrNode]) - 1:
            # stop the animation
            anim.flagOuterKeyReached = True
            # indicate that it would be the highest key inside the node
            anim.flagNewKeyHighest = True
        # observe one key all 50 to 500 milliseconds (depending on users selection)
        elif self.root.counter != 0 and self.root.counter % round(50 / self.speed) == 0:
            # after 30 frames, switch to the following key
            anim.highlightedKey += 1
        # make all keys lightblue again all 50 to 500 milliseconds (depending on users selection)
        if self.root.counter != 0 and self.root.counter % round(50 / self.speed) == 0:
            # reset counter for next animation
            self.root.counter = 0
            # set all keys to lightblue
            self.initializeColorKeyList()
            # if the comparison animation is over
            if anim.flagOuterKeyReached:
                # if there is still another part of the animation, trigger it
                if (anim.walkthrough + 1) < len(anim.checkNodes):
                    # switch to the next animation = next node
                    anim.walkthrough += 1                ##'########## !!!!!!!!!!!!!!!!!!!!!!!!!!
                    print(anim.walkthrough)
                    # ref-coloring
                    # if the key would be the highest in the node
                    if anim.flagNewKeyHighest:
                        # paint the outer right ref green 
                        # = the found path
                        self.colorRefList[anim.checkNodes[anim.walkthrough - 1] * (2 * self.k + 1) + anim.highlightedKey + 1] = "green"
                    # if the key is not the highest in the node
                    else:
                        # paint the ref left from the higher key green
                        # = the found path
                        self.colorRefList[anim.checkNodes[anim.walkthrough - 1] * (2 * self.k + 1) + anim.highlightedKey] = "green"
                    # reset highlighted key
                    anim.highlightedKey = 0    
                    # reset flags
                    anim.flagOuterKeyReached = False
                    anim.flagNewKeyHighest = False    
                # no other part of the animation left
                else:
                    # update the graph
                    # -> needed for key
                    anim.updateNewAnimation()
                    self.updateGraph()
                    self.initializeColorRefList()

    # draw whole tree including all part graphs
    def _update_graph(self, frame):
        # get the selected speed from the user
        self.speed = self.scale.get()
        # append the selected speed to the current animation's speed [pixels per iteration]
        self.currentAnimation.animationSpeed = 0.02 * self.speed
        # get the bounding box of the subplot in pixels
        bbox = self.ax.get_window_extent().transformed(self.fig.dpi_scale_trans.inverted())
        # get the width and height of the subplot in pixels
        width, height = bbox.width, bbox.height
        if len(self.nodesList) == 1:
            height *= 5
            width *= 5
        # Remove plot elements from the previous frame
        self.ax.clear()
        # background color for subplot area
        self.ax.set_facecolor('lightgray')
        # transparent color for vertex
        #vertex_color_transparent = [(0, 0, 0, 0) for i in range(self.gNodes.vcount())]
        # define Nodes-plot
        ig.plot(
            # nodes graph
            self.gNodes,
            # targetted subplot
            target = self.ax,
            # node Width (calculation in constructor)     
            vertex_width = self.nodeWidth,
            # choose height = width of 2 refs
            vertex_height = 4 * self.refWidth,
            # white color because nodes will be overlayed
            vertex_color = 'white',
            # appendself. style
            **self.visual_style
        )
        # define Refs-Aid-plot
        ig.plot(
            # refs graph
            self.gRefsAid,
            # targetted subplot
            target = self.ax,
            # width of refs aid = refWidth * 0.5
            # -> edges really stick in the centre of a ref
            vertex_width = 0.5 * self.refWidth,
            # choose height very low to force the edge to stick at the bottom of a ref
            vertex_height = 0.001 * self.refWidth,
            # gray color emblematic of refs
            vertex_color = "gray",
            # append style
            **self.visual_style
        )
        # define Refs-plot
        ig.plot(
            # refs graph
            self.gRefs,
            # targetted subplot
            target = self.ax,
            # width of refs
            vertex_width = self.refWidth,
            # choose height = width of 2 refs
            vertex_height = 4 * self.refWidth,
            # gray color emblematic of refs
            vertex_color = self.colorRefList,
            # append style
            **self.visual_style
        )
        # define Keys-plot
        ig.plot(
            # keys graph
            self.gKeys,
            # targetted subplot
            target = self.ax,
            # width of refs
            vertex_width = self.keyWidth,
            # choose height = width of 2 refs
            vertex_height = 4 * self.refWidth,
            # gray color emblematic of refs
            vertex_color = self.colorKeyList,
            # formula for dynamically resizing the labels, so they are perfectly fitting into the node
            # width and height depend on the axes of the graph
            vertex_label_size = 0.98 * math.sqrt(width) * math.sqrt(height),
            # append style
            **self.visual_style, 
        )
        # check which animation is currently performed
        if self.currentAnimation.type == 1:
            # insert
            self.animation1(width, height)
        elif self.currentAnimation.type == 2:
            # search
            self.animation2()
        # count all elements of the graph
        nhandles = 2 + 2 * len(self.keyLabels) + len(self.xGNodes) + len(self.xGRefs) + len(self.xGRefsAid) + len(self.edgesListTupel)
        # choose all children from the graph to display the whole graph
        handles = self.ax.get_children()[:nhandles]
        # return elements to be displayed
        return handles
        
    # run the graph-animation
    def runAnimation(self):
        # define animation
        # animation on the figure
        # updating function is _update_graph
        # blitting is deactivated to enable the graph to grow and shrink dynamically
        anim = animation.FuncAnimation(self.fig, self._update_graph, interval=1, blit=False, cache_frame_data=False)
        # start the tkinter window
        Tk.mainloop()
