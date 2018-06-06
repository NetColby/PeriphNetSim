# Agent Simulator
#
# Emmett Burns & Selim Hassairi
# June 2018

import math

class Agent:
    def __init__(self, x, y, canvas, pt):
        self.pt = pt
        self.canvas = canvas
        self.x, self.y = x, y
        self.moves = False

    def get_coords(self):
        # return a tuple with x y coordinates
        return (self.x, self.y)

    def get_coords_for_print(self):
        # return a tuple with x y coordinates converted to int
        return (int(self.x), int(self.y))

    def get_pt(self):
        # return tkinter pt reference for display canvas
        return self.pt

    def set_coords(self, x, y):
        # setter method for coordinates
        self.x = x
        self.y = y

    def move(self, x, y):
        # move drone object by unit vector in direction x/y
        magnitude = math.hypot(x, y)

        x = x/magnitude
        y = y/magnitude

        self.canvas.move(self.get_pt(), x, y)
        self.set_coords(self.x + x, self.y + y)

    def doesMove(self):
        return self.moves