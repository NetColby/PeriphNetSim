# Communication Model - Probabilistic

# Created by Selim Hassairi

# June 2018

from .CommunicationModel import *
import math
import random

class Probabilistic(CommunicationModel):

    def __init__(self, Rs=70, Ru=30, omega=.02, beta=1):
        CommunicationModel.__init__(self)
        self.Rs = Rs
        self.Ru = Ru
        self.communicationRange = Rs + Ru
        self.targetDist = self.communicationRange - self.communicationRange/12
        self.minDist = self.communicationRange - self.communicationRange/2
        #self.communicationRange = int(self.targetDist)
        self.omega = omega
        self.beta = beta
        self.materials = {"concrete":2, "wood" : 1.5, 'tree' : 1.1 }
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

        # Calculating the communication State
        a = euclidianDist - (self.Rs - self.Ru)
        # print("a = " + str(a))
        if euclidianDist <= self.Rs-self.Ru:
            # print("veryclose")
            return True

        elif euclidianDist > self.Rs + self.Ru:
            # print("toofar")
            return False

        else:
            # print("proba calculations")
            p = math.exp(1)**(-self.omega*(a**(self.beta*penalty)))
            attempt = random.random()
            # if penalty != 1:
            #     print(p,attempt)

            if attempt <= p :
                # print("True")
                return True
            else :
                # print("False")
                return False
