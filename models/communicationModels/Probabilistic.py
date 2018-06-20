# Communication Model - Probabilistic

# Created by Selim Hassairi

# June 2018

from .CommunicationModel import *
import math
import random

class Probabilistic(CommunicationModel):

    def __init__(self, Rs=70, Ru=30, omega=1, beta=1):
        CommunicationModel.__init__(self)
        self.Rs = Rs
        self.Ru = Ru
        self.communicationRange = Rs + Ru
        self.omega = omega
        self.beta = beta

        def attemptCommunication(self, euclidianDist):
            # print("proba attempt")
            a = euclidianDist - (self.Rs - self.Ru)

            if euclidianDist <= self.Rs-self.Ru:
                return True

            elif euclidianDist > self.Rs + self.Ru:
                return False

            else:
                p = math.exp**(sefl.omega*(a**self.beta))
                attempt = random.random()
                if attempt <= p :
                    return True
                else :
                    return False
