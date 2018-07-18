from abc import ABC, abstractmethod
import math
from ..Drone import Drone


class AlgorithmProvider(ABC):

	def __init__(self, drones):
		self.drones = drones
		super().__init__()

	def run(self, drone, obstacles, tarea):
		if type(drone) is Drone:
			moveConsumption = drone.getMoveConsumption()
			batteryLevel = drone.get_battery_level()
			distClosestBaseStation,coordsClosestBaseStation,bs = drone.getDistClosestBaseStation(self.drones)


			# ##### Undestand the situation
			# # If drone is about to run out of battery, make it go back to recharge
			if moveConsumption * distClosestBaseStation > batteryLevel and moveConsumption * distClosestBaseStation < batteryLevel + 5 and drone.getHeading() == "Free":
			  drone.setHeading("Base")
			  drone.setAnchor(drone.getCoords())
			
			# If close to Base Station, give battery back and set headed to Anchor
			if distClosestBaseStation < 20 and drone.getHeading() == "Base":
				  drone.setBatteryLevel(300)
				  drone.setHeading("Idle")

			# If back to anchor point, then quit Anchor mode
			if drone.getHeading() == "Anchor" :
				  if self.inNeighborhood(drone.getCoords(), drone.getAnchor()):
					  drone.setHeading("Free")
					  drone.setAnchor(None)
					  drone.setCommunicating(True)
			##### Action
			if drone.getHeading() == "Free":
				  self.individualRun(drone, obstacles, tarea)

			elif drone.getHeading() == "Base":
				self.moveToCoords(drone, coordsClosestBaseStation)

			elif drone.getHeading() == "Anchor":
				  # print("Coming back to Anchor")
				  self.moveToCoords(drone, drone.getAnchor())

			# self.individualRun(drone, obstacles, tarea)



	@abstractmethod
	def individualRun(self, drone):
		pass

	def moveToCoords(self, drone, coords):
		dist   = ((drone.getCoords()[0] - coords[0])**2 + (drone.getCoords()[1] - coords[1])**2	  )**.5
		dx = coords[0] - drone.getCoords()[0]
		dy = coords[1] - drone.getCoords()[1]

		magnitude = ( dx**2 + dy**2)**0.5
		# print("moving", dx, dy )
		drone.move(dx/magnitude, dy/magnitude)

	# retrun True if a given obj is in the Neighborhood of a dest object
	def inNeighborhood(self, obj, dest):
		dx = dest[0] - obj[0]
		dy = dest[1] - obj[1]

		magnitude = ( dx**2 + dy**2)**0.5

		if magnitude < 2 :
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
