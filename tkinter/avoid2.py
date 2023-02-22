import tkinter as tk
import random

HEIGHT = 500
WIDTH = 800
BALL_RADIUS = 20
BALL_COLOR = "#ff6600"
PAD_WIDTH = 100
PAD_HEIGHT = 10
PAD_COLOR = "#0066ff"

def move_ball():
    global ball_speed_x, ball_speed_y
    canvas.move(ball, ball_speed_x, ball_speed_y)
    pos = canvas.coords(ball)
    if pos[2] >= WIDTH or pos[0] <= 0:
        ball_speed_x = -ball_speed_x
    if pos[3] >= HEIGHT or pos[1] <= 0:
        ball_speed_y = -ball_speed_y
    if pos[2] >= WIDTH:
        canvas.create_text(WIDTH/2, HEIGHT/2, text="You lose!", font=("Helvetica", 30))
    canvas.after(10, move_ball)

def move_pad(event):
    canvas.move(pad, event.x, 0)
    pos = canvas.coords(pad)
    if pos[0] <= 0:
        canvas.move(pad, -pos[0], 0)
    elif pos[2] >= WIDTH:
        canvas.move(pad, WIDTH - pos[2], 0)

root = tk.Tk()
root.title("Avoid the Ball")
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg="#00ff00")
canvas.pack()

ball = canvas.create_oval(WIDTH/2-BALL_RADIUS, HEIGHT/2-BALL_RADIUS, WIDTH/2+BALL_RADIUS, HEIGHT/2+BALL_RADIUS, fill=BALL_COLOR)
pad = canvas.create_rectangle(0, HEIGHT-PAD_HEIGHT, PAD_WIDTH, HEIGHT, fill=PAD_COLOR)

ball_speed_x = 4
ball_speed_y = 4

canvas.bind("<Motion>", move_pad)
canvas.focus_set()

move_ball()

root.mainloop()
