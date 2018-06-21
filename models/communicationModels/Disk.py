# Communication Model - Disk

# Created by Selim Hassairi

# June 2018

from .CommunicationModel import *


class Disk(CommunicationModel):

    def __init__(self, comRange):
        CommunicationModel.__init__(self)
        self.communicationRange = comRange
        self.targetDist = comRange - comRange/5
        self.minDist = comRange - comRange/2


    def attemptCommunication(self, euclidianDist):
        if euclidianDist <= self.communicationRange:
            return True
        else :
            return False
