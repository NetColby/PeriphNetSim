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
        self.neighbors = []
        self.dead = False

    def getComRange(self):
        return self.comModel.getComRange()

    def getTargetDist(self):
        return self.comModel.getTargetDist()

    def getMinDist(self):
        return self.comModel.getMinDist()

    def attemptCommunication(self, euclidianDist, middlePoint, obstacles):
        return self.comModel.attemptCommunication(euclidianDist, middlePoint, obstacles)

    def idle(self):
        pass

    def do_step(self, obstacle, tarea):
        self.algorithm_provider.run(self, obstacle, tarea)

    def move(self, x, y):
        # move drone object by unit vector in direction x/y
        self.canvas.move(self.get_pt(), x, y)
        self.set_coords(self.x + x, self.y + y)

     #returns the neighbors of the drone
    def getNeighbors(self, drones, rng):
        # returns a list of drones within communications range
        dronecoord = self.get_coords()
        drones_in_range = []
        for t in [i for i in drones if not i.dead and type(i) is Drone]:
            tcoord = t.get_coords()
            euclidian = math.hypot(dronecoord[0]-tcoord[0], dronecoord[1]-tcoord[1])

            if euclidian < rng and self is not t:
                drones_in_range.append(t)

        return drones_in_range

    #updates the neighbors field to hold the drones currently being communicating with
    def updateNeighbors(self, neighbors):
        self.neighbors = neighbors

    def doesMove(self):
        return self.moves
