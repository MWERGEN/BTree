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
        self.window.columnconfigure(2, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)
        self.window.rowconfigure(2, weight=1)
        
        # mode selection
        self.input_fields_frame = tk.Frame(master=self.window)
        self.input_fields_frame.grid(column=0, row=0, sticky="NW")
        mode_label = tk.Label(self.input_fields_frame, text="Mode:")
        mode_label.grid(column=0, row=0, sticky="W")
        self.mode = tk.StringVar()
        mode_select = tk.OptionMenu(self.input_fields_frame, self.mode, *["Simple", "CSV", "Random"])
        mode_select.grid(column=0, row=1, columnspan=5, sticky="W")
        mode_select.config(width=6)
        self.mode.set("Simple") # simple as standard mode
        
        # elements of "Simple" mode
        self.simple_input_label = tk.Label(self.input_fields_frame, text="Input:")
        self.simple_input_field = tk.Entry(self.input_fields_frame, width=6)
        self.simple_input_field.config(width=6)
        
        self.simple_action_label = tk.Label(self.input_fields_frame, text="Action:")
        self.simple_action = tk.StringVar()
        self.simple_action_select = tk.OptionMenu(self.input_fields_frame, self.simple_action, *["Insert", "Delete", "Search"])
        self.simple_action_select.config(width=6)

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
        
        self.mode.trace('w', self.mode_change)
        self.mode_change(self)
        
        
        # settings menu
        self.settings_fields_frame = tk.Frame(master=self.window)
        self.settings_fields_frame.grid(column=2, row=0, sticky="NE")
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
        self.matplot_frame = tk.Frame(master=self.window)
        self.matplot_frame.grid(column=0, row=1, columnspan=3)
        # create a scale widget for selecting the number
        self.scale = tk.Scale(self.matplot_frame, from_=1, to=10, orient=tk.HORIZONTAL)
        self.scale.grid(column=0, row=0)

        animTypeList = [0]
        treeList = [[[1], [[]], [[]]]]
        operands = []

        animation = ani.Animation(animTypeList, treeList, operands)
        self.Graph = bt.BTreeVisualization(2, 0.2, 0.03, 0.1, animation)
        #self.Graph.initializeTK()

        self.canvas = FigureCanvasTkAgg(self.Graph.fig, master=self.matplot_frame)
        self.matplot_frame.counter = 0
        self.matplot_frame.after(10, self.countNext10Milliseconds)
        self.canvas.draw()

        self.canvas.get_tk_widget().grid(column=0, row=1, sticky='WE')
        self.matplot_frame.columnconfigure(0, weight=1)
        self.matplot_frame.rowconfigure(3, weight=1)

        # Create a scrollbar
        scrollbar = ttk.Scrollbar(self.matplot_frame, orient=tk.VERTICAL, command=self.canvas.get_tk_widget().yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.canvas.get_tk_widget().configure(yscrollcommand=scrollbar.set)

        self.matplot_frame.bind("<Configure>", self.update_scroll_region)

        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_motion)

        self.window.after(0, self.Graph.initializeGraph)  # Schedule the update in the main event loop

        tk.mainloop()

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
        self.simple_action_select.grid_forget()
        
        self.select_csv_button.grid_forget()
        
        self.random_from_label.grid_forget()
        self.random_from_field.grid_forget()
        self.random_to_label.grid_forget()
        self.random_to_field.grid_forget()
        self.random_amount_legs_label.grid_forget()
        self.random_amount_legs_field.grid_forget()
        
        # create suboptions belonging to main options
        if self.mode.get() == "Simple":
            self.simple_input_label.grid(column=6, row=0, sticky="W")
            self.simple_input_field.grid(column=6, row=1, sticky="W")
            
            self.simple_action_label.grid(column=12, row=0, sticky="W")
            self.simple_action_select.grid(column=12, row=1, columnspan=5, sticky="W")
            
        elif self.mode.get() == "CSV":
            self.select_csv_button.grid(column=6, row=1, sticky="W")
            
        elif self.mode.get() == "Random":
            self.random_from_label.grid(column=6, row=0, sticky="W")
            self.random_from_field.grid(column=6, row=1, sticky="W")
            self.random_to_label.grid(column=12, row=0, sticky="W")
            self.random_to_field.grid(column=12, row=1, sticky="W")
            self.random_amount_legs_label.grid(column=18, row=0, sticky="W")
            self.random_amount_legs_field.grid(column=18, row=1, sticky="W")
            
    def confirm_input(self, *args):
        print('confirm clicked')
        # insert a random number between 1 and 9999
        self.Graph.insert(random.randint(1, 9999))
        
    def update_settings(self, *args):
        print('update clicked')
        
    def browse_files(self, *args):
        # TODO do something with file(name)
        file_name = filedialog.askopenfilename(
            initialdir="/",
            title="Select a CSV file",
            filetypes=[("CSV files", "*.csv")]
        )
        print(file_name)

        
if __name__ == '__main__':
    input_obj = Input()

