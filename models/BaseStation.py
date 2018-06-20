# BaseStation Simluator
#
#Emmett Burns & Selim Hassairi
#June 2018

import math
from .Agent import Agent
from .communicationModels.Disk import Disk


class BaseStation(Agent):
    def __init__(self, x, y, algorithmProvider, pt=None, canvas=False, comModel=None):
        Agent.__init__(self, x, y, canvas=canvas)
        if comModel == None:
            self.comModel = Disk(10)
        else :
            self.comModel = comModel
        self.pt = pt
        self.algorithm_provider = algorithmProvider
        self.dead = False

    def getComRange(self):
        return self.comModel.getComRange()


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
