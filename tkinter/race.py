import tkinter as tk
import random

# Create the main window
root = tk.Tk()
root.title("Racing Game")
root.geometry("400x600")
root.config(bg="white")

# Create a canvas to draw the road
canvas = tk.Canvas(root, bg="grey", height=500, width=400)
canvas.pack()

# Draw the road lines
line_distance = 50
for i in range(10):
    canvas.create_line(0, line_distance * i, 400, line_distance * i, fill="white")

# Create a car shape
car = canvas.create_rectangle(190, 450, 210, 470, fill="red")

# Create a function to move the car
def move_car(event):
    if event.keysym == "Up":
        canvas.move(car, 0, -10)
    elif event.keysym == "Down":
        canvas.move(car, 0, 10)
    elif event.keysym == "Left":
        canvas.move(car, -10, 0)
    elif event.keysym == "Right":
        canvas.move(car, 10, 0)

# Bind the keys to the function
root.bind("<Up>", move_car)
root.bind("<Down>", move_car)
root.bind("<Left>", move_car)
root.bind("<Right>", move_car)

# Start the game loop
root.mainloop()
