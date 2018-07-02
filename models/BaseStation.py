# BaseStation Simluator
#
#Emmett Burns & Selim Hassairi
#June 2018

import math
from .Package import Package
from .Agent import Agent
from .communicationModels.Disk import Disk

class BaseStation(Agent):
	def __init__(self, x, y, algorithmProvider, pt=None, canvas=False, comModel=None):
		Agent.__init__(self, x, y, canvas=canvas)
		if comModel == None:
			self.comModel = Disk(10)
		else :
			self.comModel = comModel
		self.pt = pt
		self.algorithm_provider = algorithmProvider
		self.neighbors = []
		self.dead = False
		self.heading = "Free"
		self.recievedBuffer = []
		self.sentBuffer = []

	# Heading
	def setHeading(self, h):
		self.heading = h

	def getHeading(self):
		return self.heading


	def getComRange(self):
		return self.comModel.getComRange()

	def getTargetDist(self):
		return self.comModel.getTargetDist()

	def getMinDist(self):
		return self.comModel.getMinDist()

	def getCoords(self):
		return (self.x, self.y)

	def attemptCommunication(self, euclidianDist, middlePoint, obstacles):
		return self.comModel.attemptCommunication(euclidianDist, middlePoint, obstacles)

	def idle(self):
		pass

	def do_step(self, obstacle, tarea):
		self.sendPackages()

	def move(self, x, y):
		# move drone object by unit vector in direction x/y
		self.canvas.move(self.get_pt(), x, y)
		self.set_coords(self.x + x, self.y + y)

	 #returns the neighbors of the drone
	def getNeighbors(self, drones, rng):
		# returns a list of drones within communications range
		dronecoord = self.get_coords()
		drones_in_range = []
		for t in [i for i in drones if not i.dead]:
			tcoord = t.get_coords()
			euclidian = math.hypot(dronecoord[0]-tcoord[0], dronecoord[1]-tcoord[1])

			if euclidian < rng and self is not t:
				drones_in_range.append(t)

		return drones_in_range

	#updates the neighbors field to hold the drones currently being communicating with
	def updateNeighbors(self, neighbors):
		self.neighbors = neighbors
		
	#receives the given message
	def recievePackage(self, package):
		if type(self) is Drone:
			self.batteryLevel -= self.recieveConsumption
		if package not in self.recievedBuffer:
			self.recievedBuffer.append(package)
		
	#sends the given message to the current neighbors
	def sendPackages(self):
		if len(self.sentBuffer) != len(self.recievedBuffer):
			if type(self) is Drone:
				self.batteryLevel -= self.sendConsumption
			for package in self.recievedBuffer:
				if package not in self.sentBuffer:
					for neighbor in self.neighbors:
						neighbor.recievePackage(package)
	
	#creates and appends a package to self.recievedBufer
	def createPackage(self, message):
		pckg = Package(message)
		self.recievedBuffer.append(pckg)
			
	def doesMove(self):
		return self.moves
