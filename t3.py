import tkinter as tk

# create a tkinter window
root = tk.Tk()

# define a function to be called every second
def my_function():
    print("Called every second")

    # check if 10 seconds have passed
    if root.counter == 10:
        root.counter = 0
        print("Called every 10 seconds")

    # increment the counter
    root.counter += 1

    # schedule the next call to my_function in 1 second
    root.after(1000, my_function)

# initialize the counter
root.counter = 0

# schedule the first call to my_function in 1 second
root.after(1000, my_function)

# start the tkinter event loop
root.mainloop()