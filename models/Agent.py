# Agent Class
#
# Emmett Burns & Selim Hassairi
# June 2018

# Agent Class : Main class of the agents in the simualtion

import math

class Agent:
    def __init__(self, x, y, canvas=None):
        self.canvas = canvas
        self.x, self.y = x, y
        self.moves = False

    def get_coords(self):
        # return a tuple with x y coordinates
        return (self.x,self.y)

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

    def assignCanvas(canvas):
        self.canvas = canvas
