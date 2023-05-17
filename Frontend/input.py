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

import tkinter as tk
from tkinter import filedialog

class Input:
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=6)
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
        self.settings_fields_frame.grid(column=1, row=0, sticky="NE")
        # Order
        self.settings_order_label = tk.Label(self.settings_fields_frame, text="Order:")
        self.settings_order_label.grid(column=0, row=0, sticky="W")
        self.settings_order_field = tk.Entry(self.settings_fields_frame, width=6)
        self.settings_order_field.grid(column=0, row=1, sticky="W")
        # Speed
        self.settings_speed_label = tk.Label(self.settings_fields_frame, text="Speed:")
        self.settings_speed_label.grid(column=1, row=0, sticky="W")
        self.settings_speed_field = tk.Entry(self.settings_fields_frame, width=6)
        self.settings_speed_field.grid(column=1, row=1, sticky="W")
        # Update button
        update_button = tk.Button(self.settings_fields_frame, text="Update", command=self.update_settings)
        update_button.grid(column=2, row=1)
        
        
        # reset button
        self.reset_button_frame = tk.Frame(master=self.window, bg="red")
        self.reset_button_frame.grid(column=0, row=1, columnspan=2, sticky="SE")
        #self.reset_button_frame.columnconfigure(0, weight=1)
        reset_button = tk.Button(self.reset_button_frame, text="Reset", command=self.update_settings, bg="red")
        reset_button.grid(column=0, row=0)
        
        
        ##################
        ##################
        #   MATPLOTLIP   #
        ##################
        ##################
        # insert matplotlib here
        # should be row=2 and column=0 of self.window
        
        tk.mainloop()
        
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

