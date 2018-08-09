#Attenuated Communication Model
#Created by Emmett Burns
#06/20/2018

# A Communication Model that implements an Attenuated Approach to communications between drones

from .CommunicationModel import CommunicationModel
import random
import math

class Attenuated(CommunicationModel):

	def __init__(self, c=100, a=1, lower=0.1, upper=1.0):
		CommunicationModel.__init__(self)
		self.constant = c
		self.alpha = a
		self.lowerBound = lower # the value is picked from the plot for f vs distance at diff alpha value
		self.upperBound = upper # we decide to use alpha = 1.4 and the lower as 0.25 and upper as 0.42
		#self.communicationRange = self.getComRange()

	def attemptCommunication(self, distance, middlePoint=None, obstcles=None):
		f = (self.constant/(distance**self.alpha))
		return f >= random.uniform(self.getBoundBasedOnDistance(self.constant), self.upperBound)

	#returns a lower so that models with varying alphas may have the same communication range
	def getBoundBasedOnDistance(self, distance):
		lowerBound = (self.constant/(distance**self.alpha))
		return lowerBound

	def getComRange(self):
		range = (self.constant/self.lowerBound)**(1/self.alpha)
		return math.floor(range)

	# get dist based on the given f value
	def getDist(self, f):
		dist = (self.constant/f)**(1/self.alpha)
		return dist

	def getMinDist(self):
		return self.getDist(self.upperBound)

	def getTargetDist(self):
		target = self.getDist(self.lowerBound)
		return target

	def getInnerRange(self):
		range = (self.constant/self.upperBound)**(1/self.alpha)
		return math.floor(range)

if __name__ == "__main__" :
	at = Attenuated(100, 1.4, 0.25, 0.42)
	print(at.getBoundBasedOnDistance(100))
	print(at.attemptCommunication(1))
	print(at.attemptCommunication(10))
	print(at.attemptCommunication(20))
	print(at.attemptCommunication(30))
	print(at.attemptCommunication(40))
	print(at.attemptCommunication(50))
	print(at.attemptCommunication(60))
	print(at.attemptCommunication(70))
	print(at.attemptCommunication(80))
	print(at.attemptCommunication(90))
	print(at.attemptCommunication(100))
	print(at.getComRange())
	print(at.getInnerRange())



	# print("1: " + str(at.attemptCommunication(1)))
# 	print("10: " + str(at.attemptCommunication(10)))
# 	print("20: " + str(at.attemptCommunication(20)))
# 	print("30: " + str(at.attemptCommunication(30)))
# 	print("40: " + str(at.attemptCommunication(40)))
# 	print("50: " + str(at.attemptCommunication(50)))
# 	print("60: " + str(at.attemptCommunication(60)))
# 	print("70: " + str(at.attemptCommunication(70)))
# 	print("80: " + str(at.attemptCommunication(80)))
# 	print("90: " + str(at.attemptCommunication(90)))
# 	print("100: " + str(at.attemptCommunication(100)))
# 	print("110: " + str(at.attemptCommunication(110)))
# 	print("120: " + str(at.attemptCommunication(120)))
# 	print("130: " + str(at.attemptCommunication(130)))
# 	print("140: " + str(at.attemptCommunication(140)))
# 	print("150: " + str(at.attemptCommunication(150)))
# 	print("160: " + str(at.attemptCommunication(160)))
# 	print("170: " + str(at.attemptCommunication(170)))
# 	print("180: " + str(at.attemptCommunication(180)))
# 	print("190: " + str(at.attemptCommunication(190)))
# 	print("200: " + str(at.attemptCommunication(200)))
