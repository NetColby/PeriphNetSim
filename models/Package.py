#Emmett Burns and Selim Hassairi
#07/02/2018
#Package.py
#format for the messages to be sent between drones and base station

import random

class Package:

	def __init__(self, message, ID=None, destinationAgentID=9999, time=64, destinationCoords=None):
		self.message = message

		if ID is None:
			self.ID = random.random()
		else:
			self.ID = ID

		if destinationAgentID==None:
			self.destinationAgentID=9999
		else:
			self.destinationAgentID = destinationAgentID

		self.hops 			= []
		self.time 			= time
		self.fresh 			= True
		self.origin 		= None
		self.used 			= False
		self.destinationCoords 	= destinationCoords

	def getDestinationAgentID(self):
		# print( "destinationAgentID",  self.destinationAgentID)
		return self.destinationAgentID

	#returns the message
	def getMessage(self):
		return self.message

	#returns the ID
	def getID(self):
		return self.ID

	#adds the given ID to the hops list
	def updateHops(self, droneID):
		self.hops.append(droneID)

	#returns the hops list
	def getHops(self):
		return self.hops

	#returns True if the droneID is in self.hops
	def inHops(self, droneID):
		return droneID in self.hops

	#returns state of the message
	def isExpired(self):
		return self.time == 0

	#decrements time by a factor of 1
	def timeStep(self):
		self.time -= 1

	#returns the fresh status
	def isFresh(self):
		return self.fresh

	#changes the self.fresh value to False
	def unfreshen(self):
		self.fresh = False

	#sets the origin to the given into¶
	def setOrigin(self, origin):
		self.origin = origin

	#returns origin
	def getOrigin(self):
		return self.origin

	def setUsed(self, used):
		self.used = used

	def __repr__(self):
		return str(self.message)

	def clone(self):
		clone = Package(self.message, self.ID, destinationAgentID= self.destinationAgentID, time=self.time, destinationCoords=self.destinationCoords)
		clone.hops = self.hops
		clone.origin = self.origin
		return clone
