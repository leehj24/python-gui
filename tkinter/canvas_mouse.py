from tkinter import *

def draw(event):
    global x0, y0
    canvas.create_line(x0, y0, event.x, event.y)
    x0,y0 = event.x, event.y
    
def down(event):
    global x0, y0
    x0, y0 = event.x, event.y
    
def up(event):
    global x0, y0
    if (x0,y0)== (event.x, event.y):
        canvas.create_line(x0,y0, x0+1, y0+1)
        
from tkinter import *
import tkinter

tk = tkinter
window = tk.Tk()
canvas = Canvas(window, width=300, height=300)

canvas.bind("<B1-Motion>",draw)
canvas.bind("<Button-1>",down)
canvas.bind("<ButtonRelease-1>",up)
canvas.pack()

window.mainloop()