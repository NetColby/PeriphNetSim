# Communication Model - Disk

# Created by Selim Hassairi

# June 2018

from .CommunicationModel import *


class Disk(CommunicationModel):

    def __init__(self, comRange):
        CommunicationModel.__init__(self)
        self.communicationRange = comRange
