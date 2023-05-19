import tkinter as tk

def on_window_resize(event):
    # Get the new window size
    width = event.width
    height = event.height

    # Configure the canvas size to fill the available space
    canvas.config(width=width, height=height)

# Create the main window
window = tk.Tk()

# Create a frame to hold the canvas
frame = tk.Frame(window)
frame.pack(fill=tk.BOTH, expand=True)

# Configure the grid to expand
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

# Create a canvas
canvas = tk.Canvas(frame, bg="white")
canvas.grid(row=0, column=0, sticky="nsew")

# Add widgets or drawings to the canvas
# ...

# Bind the event handler to window resize event
window.bind("<Configure>", on_window_resize)

# Run the main event loop
window.mainloop()
