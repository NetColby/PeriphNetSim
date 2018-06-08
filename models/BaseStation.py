# BaseStation Simluator
#
#Emmett Burns & Selim Hassairi
#June 2018

import math
from .agent import Agent

class BaseStation(Agent):
    def __init__(self, x, y, canvas, pt, algorithm_provider):
        Agent.__init__(self, x, y, canvas)
        self.pt = pt
        self.algorithm_provider = algorithm_provider
        self.dead = False

    def idle(self):
        pass

    def do_step(self, obstacle):
        self.algorithm_provider.run(self, obstacle)


    def move(self, x, y):
        # move drone object by unit vector in direction x/y
        self.canvas.move(self.get_pt(), x, y)
        self.set_coords(self.x + x, self.y + y)

    def doesMove(self):
        return self.moves
