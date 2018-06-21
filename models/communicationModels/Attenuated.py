#Attenuated Communication Model
#Created by Emmett Burns
#06/20/2018

from CommunicationModel import CommunicationModel
import random

class Attenuated(CommunicationModel):

	def __init__(self, c=1, a=1, lower=55, upper=90):
		CommunicationModel.__init__(self)
		self.constant = c
		self.alpha = a
		self.lowerBound = lower
		self.upperBound = upper
		self.communicationRange = self.getRange()

	def attemptCommunication(self, distance):
		f = (self.constant/(distance**self.alpha))
		return f >= random.randint(self.lowerBound, self.upperBound)
		
	def getRange(self):
		range = (self.constant/self.lowerBound)**(1/self.alpha)
		return int(range)
		
	def getInnerRange(self):
		range = (self.constant/self.upperBound)**(1/self.alpha)
		return range

if __name__ == "__main__" :
	at = Attenuated(10000, 1.1)
	print(at.attemptCommunication(100))
	print(at.getRange())
	print(at.getInnerRange())