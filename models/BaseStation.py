# BaseStation Class
#
#Emmett Burns & Selim Hassairi
#June 2018

# BaseStation Class, child of Agent, that has move and communication functions

import math
from .Package import Package
from .Agent import Agent
from .communicationModels.Disk import Disk

class BaseStation(Agent):
	def __init__(self, x, y, algorithmProvider, pt=None, canvas=False, comModel=None, agentID=8888):
		Agent.__init__(self, x, y, canvas=canvas)
		if comModel == None:
			self.comModel = Disk(10)
		else :
			self.comModel = comModel
		self.pt = pt
		self.algorithm_provider = algorithmProvider
		self.neighbors = []
		self.comNeighbors = []
		self.dead = False
		self.heading = "Free"		#Heading of the drone, free is standard and uses algorithms
		self.communicating = True   #Boolean to check if should communicate PACKAGES or not
		self.recievedBuffer = []	#Temporary buffer that receives the packages and adds them or not to the sent buffer
		self.sentBuffer = []		#Buffer that keeps the history of all sent packages
		self.agentID = agentID      #Unique agent ID
		self.absoluteID = agentID   #ID of the drone that it is supposed to be (BS do not have "clones")
		self.action = []			#Contains the action information that is recieved from packages if this agent is the destination
		self.rescued = {}			#List of the drones that have been rescued and the amount of times they have been rescued
		self.garage = []			#List of drones back to the base station, idling
		#fields for keeping track of battery usage
		self.moveUsage = 0
		self.idleUsage = 0
		self.sendUsage = 0
		self.recieveUsage = 0

	def getGarage(self):
		return self.garage

	def get_battery_level(self):
		# return the current battery level of the drone
		return "N/A"

	def getAgentID(self):
		return self.agentID

	# Heading
	def setHeading(self, h):
		# if h == "Anchor":
		# 	self.communicating = False
		self.heading = h

	def getHeading(self):
		return self.heading

	# communicating
	def setCommunicating(self, c):
		self.communicating = c

	def isCommunicating(self):
		return self.communicating



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

	def do_step(self, obstacles, tarea):
		self.algorithm_provider.updateNeighbors(self, obstacles)
		self.algorithm_provider.updateComNeighbors(self, obstacles)
		# self.sendPackagesTargeted()
		self.sendPackagesToAll()

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

	#updates the neighbors field to hold the drones currently being taken into consideration while moving
	def updateNeighbors(self, neighbors):
		self.neighbors = neighbors

	#updates the neighbors field to hold the drones currently being communicating with
	def updateComNeighbors(self, neighbors):
		self.comNeighbors = neighbors


	#receives the given message
	def recievePackage(self, package):
		# Take away battery for receiving a package
		if type(self) is not BaseStation:
			self.batteryLevel -= self.recieveConsumption
			self.recieveUsage += self.recieveConsumption

		# Add self to hops
		package.hops.append(self.absoluteID)

		# Cloning and sending a package
		tempPackage = package.clone()
		self.recievedBuffer.append(tempPackage)


		# If the package received concerns this agent, then process the demand
		if package.getDestinationAgentID() == self.agentID :
			self.action = self.analyzePackage(package)

	#sends the given message to the current neighbors
	def sendPackagesToAll(self):

		tempRecievedBuffer = self.recievedBuffer.copy()

		# Send packages
		sentAPackage = False
		for package in tempRecievedBuffer:
			sentAPackage = True
			#updates rescued
			if package.message[0:6] == "Dyingg" and package.used == False:
				if self.rescued.get(package.getOrigin()) == None:
					self.rescued[package.getOrigin()] = 1
					package.setUsed(True)
				else:
					self.rescued[package.getOrigin()] += 1
					package.setUsed(True)



			# Send the not fresh
			for neighbor in self.comNeighbors:
				if not package.isFresh():
					if neighbor.hasntRecieved(package):
						# print("pckg sent to ", neighbor.agentID)
						neighbor.recievePackage(package)
					# else :
					# 	print("already receive package")

			# Update so that the not fresh are in the fresh
			if not package.isFresh():
				self.recievedBuffer.remove(package)
				# print("adding to sent")
				self.sentBuffer.append(package)

			# unfreshen the packages for the following step
			if package.isFresh():
				package.unfreshen()


		# Delete expired packages
		for package in self.sentBuffer:
			package.timeStep()
			if package.isExpired():
				self.sentBuffer.remove(package)

		# Derement the battery
		if type(self) is not BaseStation and sentAPackage:
			self.batteryLevel -= self.sendConsumption
			self.sendUsage += self.sendConsumption

		# Print
		# print("Drone ID #" , self.agentID, " :  sent ", self.sentBuffer, " recieved ",self.recievedBuffer, self.heading)

	#sends the given message to the current neighbors
	def sendPackagesTargeted(self):
		# Create a copy
		tempRecievedBuffer = self.recievedBuffer.copy()

		# Send packages
		sentAPackage = False
		for package in tempRecievedBuffer:
			sentAPackage = True

			#updates rescued
			if package.message[0:6] == "Dyingg" and package.used == False:
				if self.rescued.get(package.getOrigin()) == None:
					self.rescued[package.getOrigin()] = 1
					package.setUsed(True)
				else:
					self.rescued[package.getOrigin()] += 1
					package.setUsed(True)

			###
			# Find drones closest to target and store them in a List
			tempDroneList = self.comNeighbors.copy()
			neighbor = self.sendPackageToClosestToTarget(tempDroneList, package)


			###


			# Send the not fresh
			if not package.isFresh():
				if neighbor.hasntRecieved(package):
					# print("pckg sent to ", neighbor.agentID)
					neighbor.recievePackage(package)

				# else :
				# 	print("already receive package")

			# Update so that the not fresh are in the fresh
			if not package.isFresh():
				self.recievedBuffer.remove(package)
				# print("adding to sent")
				self.sentBuffer.append(package)

			# unfreshen the packages for the following step
			if package.isFresh():
				package.unfreshen()


		# Delete expired packages
		for package in self.sentBuffer:
			package.timeStep()
			if package.isExpired():
				self.sentBuffer.remove(package)

		# Derement the battery
		if type(self) is not BaseStation and sentAPackage:
			self.batteryLevel -= self.sendConsumption
			self.sendUsage += self.sendConsumption



		# Print
		# print("Drone ID #" , self.agentID, " :  sent ", self.sentBuffer, " recieved ",self.recievedBuffer, self.heading)

	def sendPackageToClosestToTarget(self, tempDroneList, package):
		# Derement the battery
		if type(self) is not BaseStation:
			self.batteryLevel -= self.sendConsumption
			self.sendUsage += self.sendConsumption

		closestDrone = tempDroneList[0]
		tempDroneList.pop(0)

		# For loop to find drone closest to target
		for drone in tempDroneList:
			droneAndTargetDist 			= self.euclidianDist(drone.getCoords(), package.destinationCoords)
			closestDroneAndTargetDist 	= self.euclidianDist(closestDrone.getCoords(), package.destinationCoords)
			if (droneAndTargetDist,closestDroneAndTargetDist) != (None,None) :
				if droneAndTargetDist < closestDroneAndTargetDist:
					closestDrone = drone

		# Take care of if drone is in hops
		if closestDrone not in package.hops:
			return closestDrone

		else:
			if not tempDroneList:
				print("RECURSION ERRORRRRRRRRR")
				exit()
			tempDroneList.remove(closestDrone)
			sendPackageToClosestToTarget(tempDroneList)
		###



	#creates and appends a package to self.recievedBuffer
	def createPackage(self, message, destinationAgentID=None, origin=None, destinationCoords=(999,999)):
		pckg = Package(message, destinationAgentID=destinationAgentID, destinationCoords=destinationCoords)
		pckg.setOrigin(origin)
		pckg.hops.append(self.agentID)
		self.recievedBuffer.append(pckg)

	# Parses the message and gets the information out
	def analyzePackage(self,package):
		list = package.getMessage().split("&")
		return list

	def checkIfConcerned(self):
		temp = False
		for pckg in self.recievedBuffer:
			if pckg.getDestinationAgentID() == self.agentID:
				self.action = self.analyzePackage(pckg)
				temp = True
		return temp

	#tells whether the given package has been received or not
	def hasntRecieved(self, package):
		for pckg in self.sentBuffer:
			if pckg.getID() == package.getID():
				return False

		for pckg in self.recievedBuffer:
			if pckg.getID() == package.getID():
				return False

		return True

	def doesMove(self):
		return self.moves

	def euclidianDist(self, x, y):
		dx = x[0] - y[0]
		dy = x[1] - y[1]

		return math.hypot(dx, dy)
