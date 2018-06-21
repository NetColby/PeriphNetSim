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
        self.targetDist = self.communicationRange - self.communicationRange/24
        self.minDist = self.communicationRange - self.communicationRange/16
        self.omega = omega
        self.beta = beta

    def attemptCommunication(self, euclidianDist):
        # print("____proba attempt")
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
            p = math.exp(1)**(-self.omega*(a**self.beta))
            attempt = random.random()
            print(p,attempt)
            if attempt <= p :
                # print("True")
                return True
            else :
                # print("False")
                return False
