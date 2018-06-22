#Attenuated Communication Model
#Created by Emmett Burns
#06/20/2018

from CommunicationModel import CommunicationModel
import random
import math

class Attenuated(CommunicationModel):

	def __init__(self, c=1, a=1, lower=55, upper=90):
		CommunicationModel.__init__(self)
		self.constant = c
		self.alpha = a
		self.lowerBound = lower
		self.upperBound = upper
		#self.communicationRange = self.getComRange()

	def attemptCommunication(self, distance):
		f = (self.constant/(distance**self.alpha))
		return f #>= random.randint(self.lowerBound, self.upperBound)

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
	at = Attenuated(100, 0.5)
	print("1: " + str(at.attemptCommunication(1)))
	print("10: " + str(at.attemptCommunication(10)))
	print("20: " + str(at.attemptCommunication(20)))
	print("30: " + str(at.attemptCommunication(30)))
	print("40: " + str(at.attemptCommunication(40)))
	print("50: " + str(at.attemptCommunication(50)))
	print("60: " + str(at.attemptCommunication(60)))
	print("70: " + str(at.attemptCommunication(70)))
	print("80: " + str(at.attemptCommunication(80)))
	print("90: " + str(at.attemptCommunication(90)))
	print("100: " + str(at.attemptCommunication(100)))
	print("110: " + str(at.attemptCommunication(110)))
	print("120: " + str(at.attemptCommunication(120)))
	print("130: " + str(at.attemptCommunication(130)))
	print("140: " + str(at.attemptCommunication(140)))
	print("150: " + str(at.attemptCommunication(150)))
	print("160: " + str(at.attemptCommunication(160)))
	print("170: " + str(at.attemptCommunication(170)))
	print("180: " + str(at.attemptCommunication(180)))
	print("190: " + str(at.attemptCommunication(190)))
	print("200: " + str(at.attemptCommunication(200)))
