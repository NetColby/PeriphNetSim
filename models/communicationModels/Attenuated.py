#Attenuated Communication Model
#Created by Emmett Burns
#06/20/2018

from .CommunicationModel import CommunicationModel
import random
import math

class Attenuated(CommunicationModel):

	def __init__(self, c=1, a=1, lower=55, upper=90):
		CommunicationModel.__init__(self)
		self.constant = c
		self.alpha = a
		self.lowerBound = lower
		self.upperBound = upper
		self.communicationRange = self.getComRange()

	def attemptCommunication(self, distance):
		f = (self.constant/(distance**self.alpha))
		return f >= random.randint(self.lowerBound, self.upperBound)

	def getComRange(self):
		range = (self.constant/self.lowerBound)**(1/self.alpha)
		return math.floor(range)

	def getMinDist(self):
		return self.getInnerRange()

	def getTargetDist(self):
		target = (self.getComRange() + self.getMinDist()) / 2
		return target
		
	def getInnerRange(self):
		range = (self.constant/self.upperBound)**(1/self.alpha)
		return math.floor(range)

if __name__ == "__main__" :
	at = Attenuated(10000, 1.1)
	print(at.attemptCommunication(100))
	print(at.getRange())
	print(at.getInnerRange())
