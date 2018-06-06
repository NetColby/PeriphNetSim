# Drone Simluator
#
# CP Majgaard & Theo Satloff
# January 2018

import math

class Drone:
    def __init__(self, x, y, canvas, pt, algorithm_provider):
        self.pt = pt
        self.canvas = canvas
        self.x, self.y = x, y
        self.battery_level = 100.0
        self.algorithm_provider = algorithm_provider
        self.dead = False
        #allows the distinguishing between base stations and drones when they are in the same list

    def get_battery_level(self):
        # return the current battery level of the drone
        return self.battery_level

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
        self.battery_level -= self.algorithm_provider.config.move_consumption
        self.update_life_state()

    def idle(self):
        self.battery_level -= self.algorithm_provider.config.idle_consumption
        self.update_life_state()

    def update_life_state(self):
        if self.battery_level < 0.5:
            self.dead = True
            self.canvas.itemconfig(self.pt, fill="red")

    def do_step(self):
        if not self.dead:
            self.algorithm_provider.run(self)
