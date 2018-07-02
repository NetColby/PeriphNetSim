#Emmett Burns and Selim Hassairi
#07/02/2018
#Package.py
#format for the messages to be sent between drones and base station

class Package:
	
	def __init__(self, message, ID, time=64):
		self.message = message
		self.ID = ID
		self.hops = []
		self.time = time
		
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