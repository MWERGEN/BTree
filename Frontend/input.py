#   Created for BTree-MTT on 10.04.23
#
#   Creator: Tim Steiner
#
#   Task: 
#
#   Editors:
#       1.  Tim Steiner on 10.04.23
#       2.  Thorben Schabel 17.05.23
#
###############################################
#
#   File description:
#       - GUI for input 
#

import random
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from Frontend import bTreeVisualization as bt
from Frontend import anim as ani
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import threading

class Input:
    def __init__(self) -> None:
        self.window = tk.Tk()

        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)
        self.window.columnconfigure(2, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)
        self.window.rowconfigure(2, weight=1)

        self.mode = tk.IntVar()
        self.mode.set(1)  # initializing the choice, i.e. Python
        self.action = tk.IntVar()
        self.action.set(1)  # initializing the choice, i.e. Python
        
        # mode selection
        self.input_fields_frame = tk.Frame(master=self.window)
        self.input_fields_frame.grid(column=0, row=0, sticky="NW")
        mode_label = tk.Label(self.input_fields_frame, text="Mode:")
        mode_label.grid(column=0, row=0, sticky="W")
        ### Radio Buttons for mode-selection
        # standard: simple mode = insert, search, delete a specific key
        self.radio_simple = tk.Radiobutton(self.input_fields_frame, 
                                            text="Simple",
                                            padx = 20, 
                                            variable=self.mode, 
                                            command=self.mode_change,
                                            value=1).grid(column=0, row=1, columnspan=5, sticky="W")
        # csv mode = read a tree from a csv file
        self.radio_csv = tk.Radiobutton(self.input_fields_frame, 
                                            text="CSV",
                                            padx = 20, 
                                            variable=self.mode, 
                                            command=self.mode_change,
                                            value=2).grid(column=0, row=2, columnspan=5, sticky="W")
        # random mode = insert random keys
        self.radio_random = tk.Radiobutton(self.input_fields_frame, 
                                            text="Random",
                                            padx = 20, 
                                            variable=self.mode, 
                                            command=self.mode_change,
                                            value=3).grid(column=0, row=3, columnspan=5, sticky="W")
        
        # elements of "Simple" mode
        self.simple_input_label = tk.Label(self.input_fields_frame, text="Input:")
        self.simple_input_field = tk.Entry(self.input_fields_frame, width=6)
        self.simple_input_field.config(width=6)
        
        self.simple_action_label = tk.Label(self.input_fields_frame, text="Action:")
        #self.simple_action = tk.StringVar()
        #self.simple_action_select = tk.OptionMenu(self.input_fields_frame, self.simple_action, *["Insert", "Delete", "Search"])
        #self.simple_action_select.config(width=6)
        ### Radio Buttons for action-selection
        # standard: simple mode = insert, search, delete a specific key
        self.radio_action_insert = tk.Radiobutton(self.input_fields_frame, 
                                                    text="Insert",
                                                    padx = 20, 
                                                    variable=self.action, 
                                                    command=self.mode_change,
                                                    value=1)
        # csv mode = read a tree from a csv file
        self.radio_action_search = tk.Radiobutton(self.input_fields_frame, 
                                                    text="Search",
                                                    padx = 20, 
                                                    variable=self.action, 
                                                    command=self.mode_change,
                                                    value=2)
        # random mode = insert random keys
        self.radio_action_delete = tk.Radiobutton(self.input_fields_frame, 
                                                    text="Delete",
                                                    padx = 20, 
                                                    variable=self.action, 
                                                    command=self.mode_change,
                                                    value=3)

        # elements of "CSV" mode
        self.select_csv_button = tk.Button(self.input_fields_frame, text = "Browse Files", command = self.browse_files)
        
        # elements of "Random" mode
        self.random_from_label = tk.Label(self.input_fields_frame, text="From:")
        self.random_from_field = tk.Entry(self.input_fields_frame, width=6)
        self.random_from_field.config(width=6)
        self.random_to_label = tk.Label(self.input_fields_frame, text="To:")
        self.random_to_field = tk.Entry(self.input_fields_frame, width=6)
        self.random_to_field.config(width=6)
        self.random_amount_legs_label = tk.Label(self.input_fields_frame, text="Amount of legs:")
        self.random_amount_legs_field = tk.Entry(self.input_fields_frame, width=6)
        self.random_amount_legs_field.config(width=6)
        
        # confirm button that is always present
        confirm_button = tk.Button(self.input_fields_frame, text="Confirm", command=self.confirm_input, bg="green")
        confirm_button.grid(column=24, row=1)
        
        #self.mode.trace('w', self.mode_change)
        self.mode_change(self)
        
        # settings menu
        self.settings_fields_frame = tk.Frame(master=self.window)
        self.settings_fields_frame.grid(column=1, row=0, sticky="NE")
        # Order
        self.settings_order_label = tk.Label(self.settings_fields_frame, text="Order:")
        self.settings_order_label.grid(column=0, row=0, sticky="W")
        self.settings_order_field = tk.Entry(self.settings_fields_frame, width=6)
        self.settings_order_field.grid(column=0, row=1, sticky="W")
        # Speed
        self.settings_speed_label = tk.Label(self.settings_fields_frame, text="Speed:")
        self.settings_speed_label.grid(column=2, row=0, sticky="W")
        self.settings_speed_field = tk.Entry(self.settings_fields_frame, width=6)
        self.settings_speed_field.grid(column=2, row=1, sticky="W")
        # Update button
        update_button = tk.Button(self.settings_fields_frame, text="Update", command=self.update_settings)
        update_button.grid(column=3, row=1)
        
        
        # reset button
        self.reset_button_frame = tk.Frame(master=self.window)
        self.reset_button_frame.grid(column=0, row=3, columnspan=3, sticky="SE")
        #self.reset_button_frame.columnconfigure(0, weight=1)
        reset_button = tk.Button(self.reset_button_frame, text="Reset", command=self.update_settings, bg="red")
        reset_button.grid(column=0, row=4)
        
        ##################
        ##################
        #   MATPLOTLIP   #
        ##################
        ##################
        # insert matplotlib here
        # should be row=1 and column=0 of self.window

        # frame for matplot content
        self.matplot_frame = tk.Frame(self.window)
        self.matplot_frame.grid(column=0, row=1, columnspan=3)
        #self.matplot_frame.pack(fill=tk.BOTH, expand=True)

        animationList = [0]
        treeList = [[[1], [[]], [[]]]]
        operands = []

        animation = ani.Animation(animationList, treeList, operands)
        self.Graph = bt.BTreeVisualization(2, 0.2, 0.03, 0.1, animation)
        #self.Graph.initializeTK()

        self.matplot_frame.counter = 0
        self.matplot_frame.after(10, self.countNext10Milliseconds)
        self.matplot_frame.columnconfigure(0, weight=1)
        self.matplot_frame.rowconfigure(0, weight=1)

        # create a scale widget for selecting the number
        self.scale = tk.Scale(self.matplot_frame, from_=1, to=20, orient=tk.HORIZONTAL)
        self.scale.grid(column=0, row=0)

        self.canvas = FigureCanvasTkAgg(self.Graph.fig, master=self.matplot_frame)
        self.canvas.get_tk_widget().grid(column=0, row=1, sticky="WE")
        #self.canvas.draw()

        # Create a scrollbar
        scrollbar = ttk.Scrollbar(self.matplot_frame, orient=tk.VERTICAL, command=self.canvas.get_tk_widget().yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        #self.canvas.get_tk_widget().configure(yscrollcommand=scrollbar.set)

        #self.matplot_frame.bind("<Configure>", self.update_scroll_region)

        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_motion)

        self.Graph.initializeGraph()

        self.commandList = []

        # Bind the event handler to window resize event
        self.matplot_frame.bind("<Configure>", self.on_window_resize)
        tk.mainloop()

    def on_window_resize(self, event):
        self.canvas.get_tk_widget().configure(width=(self.window.winfo_width() * 0.95), height=(self.window.winfo_height() * 0.75))

    def resize_canvas(self, width, height):
        # Configure the canvas size to fill the available space
        self.canvas.get_tk_widget().configure(width=self.window.winfo_width(), height=height)
        
    # raises a counter all 10 milliseconds
    # used for correct timing of animation
    def countNext10Milliseconds(self):
        # check if a method in bTreeVisualization has resetted the time counter to zero
        if self.Graph.timeCounter == 0:
            # accept the reset
            self.matplot_frame.counter = 0
        # increment the counter
        self.matplot_frame.counter += 1
        # assign counter to bTreeVisualization time counter
        self.Graph.timeCounter = self.matplot_frame.counter
        # get the selected speed from the user
        # pass it to the bTreeVisualization
        self.Graph.speed = self.scale.get()
        if self.Graph.currentAnimation.type == 0 and self.commandList:
            if self.commandList[0][0] == 1:
                self.Graph.insert(self.commandList[0][1])
            elif self.commandList[0][0] == 2:
                self.Graph.search(self.commandList[0][1])
            elif self.commandList[0][0] == 3:
                self.Graph.delete(self.commandList[0][1])
            self.commandList.pop(0)
        # schedule the next call to my_function in 1 second
        self.matplot_frame.after(10, self.countNext10Milliseconds)

    # recognizes when mouse is over the tree and displays the keys of the node the cursor is currently on
    def on_mouse_motion(self, event):
        # flag for checking if the cursor is on a key   = True
        #                                       or not  = False
        flagOnNode = False
        # index to remember the index of the node that is currently observed
        index = 0
        # self.xGNodes saves the center x position of the node 
        # now we have to pre-calculate the distance from the center of the node to its outer rim
        xDistCentreToEdge = self.Graph.k * (self.Graph.refWidth + self.Graph.keyWidth) + 0.5 * self.Graph.refWidth
        # self.yGNodes saves the center y position of the node 
        # now we have to pre-calculate the distance from the center of the node to edge above / underneath
        yDistCentreToEdge = 2 * self.Graph.refWidth
        # Check if the event occurred on the axis = the graph
        if event.inaxes is self.Graph.ax:
            # Iterate over all tk-widgets in the row for the hover-label
            for widget in self.matplot_frame.grid_slaves(row=4):
                # remove the old label to create a new one later on
                widget.grid_remove()
            # save x position on the graph's axis of the mouse cursor
            x = event.xdata
            # save y position on the graph's axis of the mouse cursor
            y = event.ydata
            # iterate over all nodes
            for i in self.Graph.keysList:
                # check if the cursor is in the x-range of the current observed node
                if x <= self.Graph.xGNodes[index] + xDistCentreToEdge and x >= self.Graph.xGNodes[index] - xDistCentreToEdge:
                    # check if the cursor is in the y-range of the current observed node
                    if y <= self.Graph.yGNodes[index] + yDistCentreToEdge and y >= self.Graph.yGNodes[index] - yDistCentreToEdge:
                        # cursor is on a node
                        flagOnNode = True
                        # save the array of the keys ( = i ) of the node the cursor is on
                        nodeOnHover = str(i)
                # raise index in order to check the other nodes
                index += 1
            # if the cursor is not on any node
            if not flagOnNode:
                # advice for user
                nodeOnHover = "Hover over a node to display its keys!"
            # display the label with the advice or the keys in the hovered node
            labelHover = tk.Label(self.matplot_frame,text=nodeOnHover).grid(column=0, row=4)
    
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
        
    def mode_change(self, *args):
        # delete all elements
        self.simple_input_label.grid_forget()
        self.simple_input_field.grid_forget()
        self.simple_action_label.grid_forget()
        self.radio_action_insert.grid_forget()
        self.radio_action_search.grid_forget()
        self.radio_action_delete.grid_forget()
        
        self.select_csv_button.grid_forget()
        
        self.random_from_label.grid_forget()
        self.random_from_field.grid_forget()
        self.random_to_label.grid_forget()
        self.random_to_field.grid_forget()
        self.random_amount_legs_label.grid_forget()
        self.random_amount_legs_field.grid_forget()
        
        # create suboptions belonging to main options
        if self.mode.get() == 1:
            self.simple_input_label.grid(column=6, row=0, sticky="W")
            self.simple_input_field.grid(column=6, row=1, sticky="W")
            
            self.simple_action_label.grid(column=12, row=0, sticky="W")
            self.radio_action_insert.grid(column=12, row=1, sticky="W")
            self.radio_action_search.grid(column=12, row=2, sticky="W")
            self.radio_action_delete.grid(column=12, row=3, sticky="W")
            
        elif self.mode.get() == 2:
            self.select_csv_button.grid(column=6, row=1, sticky="W")
            
        elif self.mode.get() == 3:
            self.random_from_label.grid(column=6, row=0, sticky="W")
            self.random_from_field.grid(column=6, row=1, sticky="W")
            self.random_to_label.grid(column=12, row=0, sticky="W")
            self.random_to_field.grid(column=12, row=1, sticky="W")
            self.random_amount_legs_label.grid(column=18, row=0, sticky="W")
            self.random_amount_legs_field.grid(column=18, row=1, sticky="W")
            
    def confirm_input(self, *args):
        input = self.simple_input_field.get()
        self.separate_input(input)
        print('confirm clicked')
        # if self.action.get() == 1:
        #     self.Graph.insert(int(self.simple_input_field.get()))
        # elif self.action.get() == 2:
        #     self.Graph.search(int(self.simple_input_field.get()))
        # elif self.action.get() == 3:
        #     self.Graph.delete(int(self.simple_input_field.get()))
        
    def update_settings(self, *args):
        self.Graph.reset()
        print("reset")
        
    def browse_files(self, *args):
        # TODO do something with file(name)
        file_name = filedialog.askopenfilename(
            initialdir="/",
            title="Select a CSV file",
            filetypes=[("CSV files", "*.csv")]
        )
        print(file_name)

    # takes the input
    # checks if input is valid 
    # only allows ints separated by comma or blank space
    # also interval is limited from 1 to 9999
    # if valid: creates an int list with all int inputs
    def separate_input(self, input):
        # index for iterating over string input
        index = 0
        # flag to indicate if invalid char has been recognizes
        # empty input is invalid
        if input == "":
            invalid = True
        # non-empty input is valid in the beginning
        else:
            invalid = False
        # saves the current number as a string
        currentNumStr = ""
        # list with all number from input
        inputNums = []
        # iterate over all characters in input
        while index < len(input):
            # only continue working if input is still valid
            if not invalid:
                # comma or blank space separates two input-numbers
                if input[index] == "," or input[index] == " ":
                    # check if the current number is really an int
                    if currentNumStr.isdigit():
                        # only allow ints between 0 and 9999
                        if int(currentNumStr) > 0 and int(currentNumStr) < 9999:
                            # append the current number as an int to the input List
                            inputNums.append((self.action.get(), int(currentNumStr)))
                        # invalid int
                        else:
                            # set invalid flag
                            invalid = True
                            print("invalid")
                    # reset the current number
                    currentNumStr = ""
                # if the current char is an int
                elif input[index].isdigit():
                    # add it to the current number as a string
                    currentNumStr += input[index]
                # invalid character in input
                else:
                    # set invalid flag
                    invalid = True
                    print("invalid")
            # increment index for next char
            index += 1
        # check if the current number is a digit
        # if the last character in input is a digit -> it is not appended yet
        if currentNumStr.isdigit() and not invalid:
            # only allow ints between 0 and 9999
            if int(currentNumStr) > 0 and int(currentNumStr) < 9999:
                # append the last number to the number list
                inputNums.append((self.action.get(), int(currentNumStr)))
            # invalid int
            else:
                # set invalid flag
                invalid = True
                print("invalid")
        # only continue with input if it is valid
        if not invalid:
            self.commandList.extend(inputNums)
            print(self.commandList)

        
#if __name__ == '__main__':
#    input_obj = Input()

