from abc import ABC, abstractmethod
import math
from ..Drone import Drone
from .baseToRechargeAlgorithm import BaseToRechargeAlgorithm
from .rescueMessageForReplacementAlgorithm import RescueMessageForReplacementAlgorithm


class AlgorithmProvider(ABC):

	def __init__(self, drones):
		self.drones = drones
		super().__init__()
		# self.numReplaces = 3
		# self.replacementAlgorithm = RescueMessageForReplacementAlgorithm(self.drones, numReplaces=3)
		self.replacementAlgorithm = BaseToRechargeAlgorithm(self.drones, numReplaces=3)

	def run(self, drone, obstacles, tarea):
		if type(drone) is Drone:
			###### Undestand the situation
			if self.replacementAlgorithm != None:
				# Determine initial settings and environement
				moveConsumption = drone.getMoveConsumption()
				batteryLevel = drone.get_battery_level()
				distClosestBaseStation,coordsClosestBaseStation,bs = drone.getDistClosestBaseStation(self.drones)
				baseStationInfoList = [distClosestBaseStation,coordsClosestBaseStation,bs]


				###### Make All Decisions depending on the replacementAlgorithm chosen
				self.replacementAlgorithm.makeDecisions(drone, obstacles, tarea, baseStationInfoList)




				##### Action
				# If back to anchor point, then quit Anchor mode
				if drone.getHeading() == "Anchor" :
					if self.inNeighborhood(drone.getCoords(), drone.getAnchor()):
						drone.setHeading("Free")
						drone.setAnchor(None)

				# Move according to algorithm
				if drone.getHeading() == "Free":
					self.individualRun(drone, obstacles, tarea)

				# Move back to the base station
				elif drone.getHeading() == "Base":
					self.moveToCoords(drone, coordsClosestBaseStation)

				# Move to the anchor point
				elif drone.getHeading() == "Anchor":
					self.moveToCoords(drone, drone.getAnchor())

			else :
				self.individualRun(drone, obstacles, tarea)



	@abstractmethod
	def individualRun(self, drone):
		pass

	def moveToCoords(self, drone, coords):
		dist   = ((drone.getCoords()[0] - coords[0])**2 + (drone.getCoords()[1] - coords[1])**2	  )**.5
		dx = coords[0] - drone.getCoords()[0]
		dy = coords[1] - drone.getCoords()[1]

		magnitude = ( dx**2 + dy**2)**0.5

		#Avoid collisions:


		drone.move(dx/magnitude, dy/magnitude)

	# retrun True if a given obj is in the Neighborhood of a dest object
	def inNeighborhood(self, obj, dest):
		dx = dest[0] - obj[0]
		dy = dest[1] - obj[1]

		magnitude = ( dx**2 + dy**2)**0.5

		if magnitude < 1 :
			return True
		else :
			return False

	def get_drones_within_com_range(self, drone, obstacles):
		# returns a list of drones within communications range
		dronecoord = drone.get_coords()
		drones_in_range = []
		for t in [i for i in self.drones if not i.dead]:
			tcoord = t.get_coords()
			euclidian = math.hypot(dronecoord[0]-tcoord[0], dronecoord[1]-tcoord[1])
			middlePoint = ( ((dronecoord[0]+tcoord[0])/2) , (dronecoord[1]+tcoord[1])/2 )
			if drone is not t and drone.getHeading() == "Free" and t.getHeading()== "Free":
				if t.attemptCommunication(euclidian, middlePoint, obstacles):
					drones_in_range.append(t)
					drone.updateNeighbors(drones_in_range)
		# print("returned list", drones_in_range)
		return drones_in_range

	def getCommunicatingDrones(self, drone, obstacles):
		# returns a list of drones within communications range
		dronecoord = drone.get_coords()
		drones_in_range = []
		for t in [i for i in self.drones if not i.dead]:
			tcoord = t.get_coords()
			euclidian = math.hypot(dronecoord[0]-tcoord[0], dronecoord[1]-tcoord[1])
			middlePoint = ( ((dronecoord[0]+tcoord[0])/2) , (dronecoord[1]+tcoord[1])/2 )
			if drone is not t and drone.isCommunicating() and t.isCommunicating():
			# if drone is not t and drone.getHeading() == "Free" and t.getHeading()== "Free":
				if t.attemptCommunication(euclidian, middlePoint, obstacles):
					drones_in_range.append(t)
					drone.updateComNeighbors(drones_in_range)
		# print("returned list Com", drones_in_range)
		return drones_in_range



	def updateNeighbors(self, agent, obstacles):
		self.get_drones_within_com_range(agent, obstacles)

	def updateComNeighbors(self, agent, obstacles):
		self.getCommunicatingDrones(agent, obstacles)
