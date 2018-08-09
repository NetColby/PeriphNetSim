# Communication Model Abstract Class

# Created by Selim Hassairi
# June 2018

# Allows to set things up for different Communication Models implementations

class CommunicationModel:

    def __init__(self):
        self.communicationRange = None
        self.targetDist = None
        self.minDist = None
        self.materials = {"concrete": .01, "wood" : .4, 'tree' : .8}
        self.material = self.materials.get("wood")

    def getComRange(self):
        return self.communicationRange

    def getTargetDist(self):
        return self.targetDist

    def getMinDist(self):
        return self.minDist

    def attemptCommunication(self,euclidianDist, middlePoint, obstacles):
        print("THIS SHOULD NOT POP UP")
        return False
