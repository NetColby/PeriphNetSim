# Communication Model Abstrat Class

# Created by Selim Hassairi

# June 2018

class CommunicationModel:

    def __init__(self):
        self.communicationRange = None
        self.targetDist = None
        self.minDist = None

    def getComRange(self):
        return self.communicationRange

    def getTargetDist(self):
        return self.targetDist

    def getMinDist(self):
        return self.minDist

    def attemptCommunication(self,euclidianDist):
        print("THIS SHOULD NOT POP UP")
        return False
