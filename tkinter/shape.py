import tkinter as tk
import random

# create a window
root = tk.Tk()
root.title("Obstacle Avoiding Game")
root.geometry("400x400")

# create a canvas
canvas = tk.Canvas(root, bg='white', width=400, height=400)
canvas.pack()

# function to create an obstacle at a random location
def create_obstacle():
    x = random.randint(50, 350)
    y = random.randint(50, 350)
    canvas.create_rectangle(x, y, x+50, y+50, fill='red')

# button to create an obstacle
button = tk.Button(root, text="Create Obstacle", command=create_obstacle)
button.pack()

# start the tkinter event loop
root.mainloop()