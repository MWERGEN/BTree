import tkinter as tk
from tkinter import ttk

# Create a tkinter window
window = tk.Tk()

# Create a canvas
canvas = tk.Canvas(window)
canvas.grid(row=0, column=0, sticky="nsew")

# Create a frame inside the canvas to hold the content
frame = ttk.Frame(canvas)
canvas.create_window(0, 0, anchor='nw', window=frame)

# Create a scrollbar
scrollbar = ttk.Scrollbar(window, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
canvas.configure(yscrollcommand=scrollbar.set)

# Configure grid weights to allow resizing
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# Update the scrollable region when the canvas size changes
def update_scroll_region(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

canvas.bind("<Configure>", update_scroll_region)

# Add your content to the frame
# ...

# Start the tkinter event loop
window.mainloop()