# Drone Simluator
#
# CP Majgaard & Theo Satloff
# January 2018
#updated by Emmett Burns & Selim Hassairi
#June 2018

import math
from .BaseStation import BaseStation

class Drone(BaseStation):
    def __init__(self, x, y, canvas, pt, algorithm_provider):
        BaseStation.__init__(self, x, y, canvas, pt, algorithm_provider)
        self.battery_level = 100.0
        self.moves = True

    def get_battery_level(self):
        # return the current battery level of the drone
        return self.battery_level

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

    def isDead(self):
        return self.dead

    def do_step(self):
        if not self.dead:
            self.algorithm_provider.run(self)
