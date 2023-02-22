import tkinter as tk
import random

class Game(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.canvas = tk.Canvas(self, width=500, height=400, bg="white")
        self.canvas.pack()
        self.player = self.canvas.create_rectangle(0, 0, 25, 25, fill="blue")
        self.canvas.move(self.player, 225, 375)
        self.obstacle = self.canvas.create_rectangle(0, 0, 50, 50, fill="red")
        self.canvas.move(self.obstacle, random.randint(0, 450), random.randint(0, 300))
        self.bind("<Left>", self.left)
        self.bind("<Right>", self.right)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)
        self.after(100, self.update)
        
    def left(self, event):
        self.canvas.move(self.player, -25, 0)
        
    def right(self, event):
        self.canvas.move(self.player, 25, 0)
        
    def up(self, event):
        self.canvas.move(self.player, 0, -25)
        
    def down(self, event):
        self.canvas.move(self.player, 0, 25)
        
    def update(self):
        player_coords = self.canvas.coords(self.player)
        obstacle_coords = self.canvas.coords(self.obstacle)
        if player_coords[0] <= obstacle_coords[2] and player_coords[2] >= obstacle_coords[0]:
            if player_coords[1] <= obstacle_coords[3] and player_coords[3] >= obstacle_coords[1]:
                self.game_over()
        self.after(100, self.update)
        
    def game_over(self):
        self.canvas.create_text(250, 200, text="Game Over!", font=("Helvetica", 24))
        self.unbind("<Left>")
        self.unbind("<Right>")
        self.unbind("<Up>")
        self.unbind("<Down>")

if __name__ == "__main__":
    game = Game()
    game.title("Obstacle Avoidance Game")
    game.mainloop()
