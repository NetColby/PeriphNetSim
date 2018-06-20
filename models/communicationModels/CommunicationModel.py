# Communication Model Abstrat Class

# Created by Selim Hassairi

# June 2018

class CommunicationModel:

    def __init__(self):
        self.communicationRange = None

    def getComRange(self):
        return self.communicationRange

    def attemptCommunication(self,euclidianDist):
        print("THIS SHOULD NOT POP UP")
        return False
