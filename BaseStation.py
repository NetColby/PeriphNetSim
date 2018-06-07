# BaseStation Simluator
#
#Emmett Burns & Selim Hassairi
#June 2018

import math
from .agent import Agent

class BaseStation(Agent):
    def __init__(self, x, y, canvas, pt, algorithm_provider):
        Agent.__init__(self, x, y, canvas, pt)
        self.algorithm_provider = algorithm_provider
        self.dead = False

    def idle(self):
        pass

    def do_step(self):
        self.algorithm_provider.run(self)