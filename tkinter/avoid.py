import tkinter as tk
import random

WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
BALL_COLOR = "red"
OBSTACLE_COLOR = "blue"
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 50

class Ball:
    def __init__(self, x, y, canvas):
        self.x = x
        self.y = y
        self.canvas = canvas
        self.ball = canvas.create_oval(x - BALL_RADIUS, y - BALL_RADIUS, x + BALL_RADIUS, y + BALL_RADIUS, fill=BALL_COLOR)

    def move(self, dx, dy):
        self.canvas.move(self.ball, dx, dy)
        self.x += dx
        self.y += dy

class Obstacle:
    def __init__(self, x, y, canvas):
        self.x = x
        self.y = y
        self.canvas = canvas
        self.obstacle = canvas.create_rectangle(x - OBSTACLE_WIDTH / 2, y - OBSTACLE_HEIGHT / 2,
                                                x + OBSTACLE_WIDTH / 2, y + OBSTACLE_HEIGHT / 2, fill=OBSTACLE_COLOR)

    def collision(self, ball):
        return (ball.x - self.x) ** 2 + (ball.y - self.y) ** 2 <= (BALL_RADIUS + OBSTACLE_WIDTH / 2) ** 2

def game_over(canvas, ball):
    canvas.create_text(WIDTH / 2, HEIGHT / 2, text="Game Over", font=("Helvetica", 24))
    ball.canvas.delete(ball.ball)

def update(canvas, ball, obstacles):
    if ball.x >= WIDTH - BALL_RADIUS or ball.x <= BALL_RADIUS:
        game_over(canvas, ball)
        return
    if ball.y >= HEIGHT - BALL_RADIUS or ball.y <= BALL_RADIUS:
        game_over(canvas, ball)
        return
    for obstacle in obstacles:
        if obstacle.collision(ball):
            game_over(canvas, ball)
            return
    dx = random.randint(-5, 5)
    dy = random.randint(-5, 5)
    ball.move(dx, dy)
    canvas.after(100, update, canvas, ball, obstacles)

def start_game(canvas, ball, obstacles):
    for obstacle in obstacles:
        canvas.delete(obstacle.obstacle)
    ball.x = WIDTH / 2
    ball.y = HEIGHT / 2
    ball.canvas.coords(ball.ball, ball.x - BALL_RADIUS, ball.y - BALL_RADIUS,
                       ball.x + BALL_RADIUS, ball.y + BALL_RADIUS)
