# Communication Model - Disk

# Created by Selim Hassairi
# June 2018

# A Communication Model that implements a Disk Approach to communications between drones

from .CommunicationModel import *
import random

class Disk(CommunicationModel):

    def __init__(self, comRange):
        CommunicationModel.__init__(self)
        self.communicationRange = comRange
        self.targetDist = comRange*1
        self.minDist = comRange*.5
        self.material = self.materials.get("concrete")


    def attemptCommunication(self, euclidianDist, middlePoint, obstacles):
        # Checking if acros an obstacle or not
        inObstcl = False
        penalty = 1
        for o in obstacles:
            if o.inObstacle(middlePoint[0],middlePoint[1]):
                inObstcl = True

        if inObstcl:
            penalty = self.material

        # Returning the communication state
        if euclidianDist <= self.communicationRange:
            if random.random() < penalty :
                return True
        else :
            return False
