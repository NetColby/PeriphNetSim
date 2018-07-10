#Emmett Burns
#06/14/18
#Simulation.py

import random

from .Drone import Drone
from .algorithms.naive_algorithm import NaiveAlgorithm
from .algorithms.naive_algorithm_obstcl_avoider import NaiveAlgorithmObstclAvoider
from .algorithms.naive_algorithm_obstcl_avoider_targetArea import NaiveAlgorithmObstclAvoiderTargetArea
from .TargetArea import targetArea
from .BaseStation import BaseStation
from .Agent import Agent
from .Obstacle import Obstacle
from .communicationModels.Disk import Disk
from .communicationModels.Probabilistic import Probabilistic
from .communicationModels.Attenuated import Attenuated

# create a class to build and manage the display
class Simulation:

	def __init__(self, width, height, numdrones, dronescoordinatesList, numbasestation,
		basestationcoordinatesList,
		tareaboolean, tareaWidth, tareaHeight, tareaCoords,
		obstclboolean, obstclWidthList, obstclHeightList, obstclCoordsList, batteryLevel, moveConsumption, idleConsumption, comList, gui=False):

		# width and height of the window (these are here because they maintain uniform spawning of the drones)
		self.initDx = width
		self.initDy = height

		# set up the application state
		self.drones = [] # list of drones with canvas point
		self.lines = [] # list of lines connecting drones
		self.data = None # will hold the raw data someday.

		# Presence or abscence of Target Area and Obstacle
		self.tareab = False
		self.obstclb = False

		self.view_tx = 0
		self.view_ty = 0

		#holds the command line arguments from run.py
		self.args = []

		#fields that hold the parameters of the simulation
		self.numdrones = numdrones
		self.dronescoordinatesList = dronescoordinatesList
		self.numbasestation = numbasestation
		self.basestationcoordinatesList = basestationcoordinatesList
		self.tareaboolean = tareaboolean
		self.tareaWidth = tareaWidth
		self.tareaHeight = tareaHeight
		self.tareaCoords = tareaCoords
		self.obstclboolean = obstclboolean
		self.obstclWidthList = obstclWidthList
		self.obstclHeightList = obstclHeightList
		self.obstclCoordsList = obstclCoordsList
		self.batteryLevel = batteryLevel
		self.moveConsumption = moveConsumption
		self.idleConsumption = idleConsumption

		# Drone ID Counter
		self.agentIDs = 0


		if comList[0] == "Disk":
			self.comModel = Disk(int(comList[1]))
		elif comList[0] == "Probabilistic":
			self.comModel = Probabilistic()
		elif comList[0] == "Attenuated":
			self.comModel = Attenuated(int(comList[1]), float(comList[2]), float(comList[3]), float(comList[4]))
		else:
			self.comModel = Disk(105)
		#field that holds whether or not to run the simulation without the GUI
		self.gui = gui

		# self.setUpSimulation(0, [], 0, [], False, 0, 0, (0, 0), True, 0, 0, (0, 0))
		if not gui:
			self.setUpSimulation( numdrones, dronescoordinatesList, numbasestation, basestationcoordinatesList, tareaboolean, tareaWidth, tareaHeight, tareaCoords, obstclboolean, obstclWidthList, obstclHeightList, obstclCoordsList)

	# Set up and run the simulation from the file settings
	def setUpSimulation(self, numdrones, dronescoordinatesList, numbasestation,
		basestationcoordinatesList, tareaboolean, tareaWidth, tareaHeight, tareaCoords,
		obstclboolean, obstclWidth, obstclHeight, obstclCoordsList):

		self.tarea = None
		if tareaboolean :
			self.createTargetArea(tareaCoords[0], tareaCoords[1], tareaWidth, tareaHeight)

		self.obstacles = []
		#temporary fix for obstclHeight and obstcleWidth not being lists

		#if the given width, height and coords lists are not the same length, the shorter lists will be lengthened to
		#the length of the longer lists by repeating the last element in the shorter lists

		if type(obstclWidth) != list:
			obstclWidthList = [int(obstclWidth)]
		if type(obstclHeight) != list:
			obstclHeightList = [int(obstclHeight)]
		if obstclboolean:
			if not( len(obstclWidthList) == len(obstclHeightList) == len(obstclCoordsList) ):
				while len(obstclWidthList) < len(obstclHeightList) or len(obstclWidthList) < len(obstclCoordsList):
					obstclWidthList.append(obstclWidthList[len(obstclWidthList)-1])
				while len(obstclHeightList) < len(obstclWidthList) or len(obstclHeightList) < len(obstclCoordsList):
					obstclHeightList.append(obstclHeightList[len(obstclHeightList)-1])
				while len(obstclCoordsList) < len(obstclWidthList) or len(obstclCoordsList) < len(obstclHeightList):
					obstclCoordsList.append(obstclCoordsList[len(obstclCoordsList)-1])
			for i in range(len(obstclWidthList)):
				self.createObstacle(obstclCoordsList[i][0], obstclCoordsList[i][1], obstclWidthList[i], obstclHeightList[i])

		# Generate drones, both specified and random
		for coords in dronescoordinatesList:
			self.createDrone(coords[0], coords[1])

		if numdrones != len(dronescoordinatesList) :
			for i in range(numdrones - len(dronescoordinatesList)):
				self.createRandomDrone()

		# Generate Base Stations, both specified and random
		for coords in basestationcoordinatesList:
			self.createBaseStation(coords[0], coords[1])

		if numbasestation != len(basestationcoordinatesList):
			for i in range(numbasestation - len(basestationcoordinatesList)) :
				pass

		# self.drones[2].createPackage("Hello", 4)
		self.drones[2].dying(self.drones)

	#creates the given number of random drones
	def createRandomDrones(self, numDrones=10):
		for i in range(numDrones):
			self.createRandomDrone()

	#creates and places a drone in a random location
	def createRandomDrone(self, event=None):
		x = None
		y = None
		while (x == None and y == None ) or (self.inObstacles(x,y) if self.obstacles!=None else False) :
			if not self.tareab :
				x = random.gauss(self.initDx/2, self.initDx/15)
				y = random.gauss(self.initDy/2, self.initDy/15)

			else:
				x = random.gauss(self.tarea.getCoords()[0], self.initDx/15)
				while x < self.tarea.getCoords()[0]-(self.tarea.getTAwidth()/2) or x > self.tarea.getCoords()[0]+(self.tarea.getTAwidth()/2):
					x = random.gauss(self.tarea.getCoords()[0], self.initDx/15)

				y = random.gauss( self.tarea.getCoords()[1], self.initDy/15)
				while y < self.tarea.getCoords()[1]-(self.tarea.getTAheight()/2) or y > self.tarea.getCoords()[1]+(self.tarea.getTAheight()/2):
					y = random.gauss(self.tarea.getCoords()[0], self.initDy/15)

		self.createDrone(x, y)

	#creates a drone at the given location
	def createDrone(self, x, y, algorithm=NaiveAlgorithmObstclAvoiderTargetArea):
		drone = Drone(x-self.view_tx, y-self.view_ty, algorithm(self.drones), comModel=self.comModel, batteryLevel=self.batteryLevel, moveConsumption=self.moveConsumption, idleConsumption=self.idleConsumption, agentID=self.agentIDs)
		self.drones.append(drone)
		# Keep track of how many drones are created
		self.agentIDs += 1
		return drone


	#creates a base station at the given location
	def createBaseStation(self, x=100, y = 100, algorithm=NaiveAlgorithmObstclAvoiderTargetArea, event=None):
		baseStation = BaseStation(x-self.view_tx, y-self.view_ty, algorithm(self.drones), comModel=self.comModel, agentID=self.agentIDs)
		self.drones.append(baseStation)
		# Keep track of how many drones are created
		self.agentIDs += 1

		return baseStation
	#creates a target area given x and y coordinates, width and height
	def createTargetArea(self, x=450, y=338, w=None, h=None, event=None):
		self.tareab = True
		self.tarea = targetArea(x, y, w, h)

	#creates an obstacle given x and y coordinates, width and height
	def createObstacle(self, x=450, y=338, w=None, h=None):
		self.obstclb = True
		del self.drones[:]
		self.obstacles.append(Obstacle(x, y, w, h))

	#returns True if the given coordinate falls within and obstacle
	def inObstacles(self, x, y):
		for obstacle in self.obstacles:
			if obstacle.inObstacle(x, y):
				return True
		return False

	#resets the simulation
	def clearData(self, event=None):
		del self.drones[:]
		self.lines = []

		if self.tareab:
			self.tareab = False
			self.tarea = None

		if self.obstclb:
			self.obstclb = False
			self.obstacles = None

		print('Simulation has been reset.')

	#updates the location of the drones based on their algorithm
	def droneStep(self):
		for drone in self.drones:
			drone.do_step(self.obstacles, self.tarea)
			concerned = drone.checkIfConcerned()
			if concerned:
				self.respond(drone)
		for drone in self.drones:
			print("Drone ID #" , drone.agentID, " :  sent ", drone.sentBuffer, " recieved ",drone.recievedBuffer, drone.heading)


	# Takes measures to answer the message (create a new drone, head back to B.S., etc..)
	def respond(self, drone):
		mainMessage = drone.action[0]
		if mainMessage == "Dyingg":
			newDrone = self.createDrone(drone.getCoords()[0]+1,drone.getCoords()[1])
			coords = drone.action[1][1:-1].split(",")
			newDrone.setAnchor((int(coords[0]), int(coords[1])))
			newDrone.setHeading("Anchor")

	#runs the simulation for the given number of steps and prints status messages to the terminal
	def multiStep(self, steps, frequency, event=None):
		#variable keeps track of the number of steps in the current simulation for printing status messages
		stepsForStatus = 0
		stringForOutputFile = self.statsToOutputFile()
		for i in range(steps):
			if frequency != 0:
				if (stepsForStatus % frequency) == 0:
					print(self.statusMessage(stepsForStatus))
			self.droneStep()
			stepsForStatus += 1
		if frequency != 0:
			if (stepsForStatus-1 % frequency) != 0:
				print(self.statusMessage(stepsForStatus))
		self.statsToOutputFile(stringForOutputFile, stepsForStatus)
		print("___New Step___")


	#prints the status of a simulation when in begins
	#set numDrones to True when it becomes necessary to display the number of drones
	def statusMessage(self, stepsForStatus):
		output = "________________________Statistics after " + str(stepsForStatus) + " steps:________________________\n"
		output += str(self.numAliveDrones()) + " drones alive.\n"
		output += "Average Energy Level: " + str(self.avgEnergyLevel()) + "\n"
# 		output += "Coverage: " + str(self.coverage(self.comModel.getComRange())) + "\n"
		output += "Uniformity: " + str(self.uniformity(self.comModel.getComRange())) + "\n\n"
		if(self.numDrones() > 0):
			output += "_________Drones_________\n"
			for agent in self.drones:
				if type(agent) is Drone:
					output += "Drone at (%.3f" % agent.get_coords()[0] + ", %.3f" %  + agent.get_coords()[1] + ") Alive: " + str(not agent.isDead()) + "\n"
		if(self.numBases() > 0):
			output += "\n______Base Station(s)______\n"
			for agent in self.drones:
				if type(agent) is BaseStation:
					output += "Base Station at " + str(agent.get_coords()) + "\n"
		if self.tareab:
			output += "\n______Target Area______\n"
			output += "Coordinates of Center: " + str(self.tarea.get_coords_for_print()) + "\n"
			output += "Width x Height: " + str(self.tarea.getAwidth()) + " x " + str(self.tarea.getAheight()) + "\n"
		if self.obstclb:
			output += "\n______Obstacle______\n"
			for obstacle in self.obstacles:
				output += "\nCoordinates of Center: (%.3f" % obstacle.get_coords()[0] + ", %.3f" % obstacle.get_coords()[1] + ")\n"
				output += "Width x Height: " + str(obstacle.getAwidth()) + " x " + str(obstacle.getAheight()) + "\n"
		return output

	#stores the initial status of the simulation and the writes the starting and final statistics to an output file when given the intiial stats
	def statsToOutputFile(self, initialStats = None, stepsForStatus=None):
		if initialStats == None:
			stats = "____________________Before Simulation of " + str(self.numDrones()) + " Drones____________________\n\n"
		else:
			stats = initialStats
			stats += "\n\n____________________After Simulation(" + str(stepsForStatus) +" steps)____________________\n\nTotal Drones:  " + str(self.numDrones()) + "\n"
		stats += "Live Drones: " + str(self.numAliveDrones()) + "\n "
		stats += "Average Energy Level: " + str(self.avgEnergyLevel()) + "\n "
		stats += "Coverage: " + str(self.coverage(self.comModel.getComRange())) + "\n "
		stats += "Uniformity: " + str(self.uniformity(self.comModel.getComRange())) + "\n "
		if(self.numDrones() > 0):
			stats += "\n_________Drones_________\n"
			for agent in self.drones:
				if type(agent) is Drone:
					stats += "Drone at (%.3f" % agent.get_coords()[0] + ", %.3f" %  + agent.get_coords()[1] + ") Alive: " + str(not agent.isDead()) + "\n"
		if(self.numBases() > 0):
			stats += "\n______Base Station(s)______\n"
			for agent in self.drones:
				if type(agent) is BaseStation:
					stats += "Base Station at " + str(agent.get_coords()) + "\n"
		if self.tareab:
			stats += "\n______Target Area______\n"
			stats += "Coordinates of Center: " + str(self.tarea.get_coords_for_print()) + "\n"
			stats += "Width x Height: " + str(self.tarea.getAwidth()) + " x " + str(self.tarea.getAheight()) + "\n"
		if self.obstclb:
			stats += "\n______Obstacle______\n"
			for obstacle in self.obstacles:
				stats += "\nCoordinates of Center: (%.3f" % obstacle.get_coords()[0] + ", %.3f" % obstacle.get_coords()[1] + ")\n"
				stats += "Width x Height: " + str(obstacle.getAwidth()) + " x " + str(obstacle.getAheight()) + "\n"
		if initialStats == None:
			return stats
		else:
			text_file = open("Output.txt", "w")
			text_file.write("%s" % stats)
			text_file.close()

	#the total time it takes the drones to cover a uniform network
	def time():
		pass

	#calculates and returns the coverage of the network
	def coverage(self, rng):
		prelimCoverage = set({})
		coverage = set({})
		for agent in self.drones:
			if type(agent) is Drone:
				droneCoverage = agent.getCoverage(rng)
				prelimCoverage = prelimCoverage.union(droneCoverage)
		#if there is a target area
		if self.tareab:
			for point in prelimCoverage:
				if self.tarea.inArea(point):
					coverage.add(point)
			totalPixelsInRange = len(coverage)
			targetAreasArea = self.tarea.getArea()
			c = (totalPixelsInRange) / targetAreasArea
		else:
			c = "No ROI (coverage incalculable)"
		return(c)

	#calculates and returns the uniformity of the network
	def uniformity(self, rng):
		total = 0
		for agent in self.drones:
			if type(agent) is Drone:
				total += agent.droneUniformity(self.drones, rng)
		output = total/self.numDrones()
		return output

	# return the average energy level of the drones
	def avgEnergyLevel(self):
		energy = 0.0
		if not self.drones:
			return energy
		for drone in self.drones:
			if type(drone) is Drone:
				energy += drone.get_battery_level()
		if self.numDrones() == 0:
			return 0
		else:
			return energy/self.numDrones()

	#returns the number of drones in the drones list
	def numDrones(self):
		numDrones = 0
		for agent in self.drones:
			if type(agent) is Drone:
				numDrones += 1
		return numDrones

	# return the num of alive drones
	def numAliveDrones(self):
		num = 0
		if self.drones:
			for drone in self.drones:
				if type(drone) is Drone and not drone.isDead():
					num += 1
		return num

	#returns the number of Base Stations in the drones list
	def numBases(self):
		numBases = 0
		for agent in self.drones:
			if type(agent) is BaseStation:
				numBases += 1
		return numBases

	#gets arguements from run.py which run.py gets from the command line
	def getArgs(self, args):
		self.args = args
		print(self.args)

	#interprets the frequency at which to print status updates to terminal
	def interpretFrequency(self):
		frequencyOfPrint = 10
		if "-F" in self.args:
			index = self.args.index("-F")
			frequencyOfPrint = int(self.args[index + 1])
		return frequencyOfPrint

	#interprets the number of steps to be gone through in runWithoutGUI()
	def interpretSteps(self):
		numberOfSteps = 10
		if "-S" in self.args:
			index = self.args.index("-S")
			numberOfSteps = int(self.args[index + 1])
		return numberOfSteps

	#interpretes whether or not to run the GUI
	def interpretGUI():
		if "-W" in self.args:
			index = self.args.index("-W")
			self.gui = False

	#runs simulation
	def main(self, iterations, steps):
		for i in range(iterations):
			self.clearData()
			self.setUpSimulation(self.numdrones, self.dronescoordinatesList, self.numbasestation,
				self.basestationcoordinatesList, self.tareaboolean, self.tareaWidth, self.tareaHeight,
				self.tareaCoords, self.obstclboolean, self.obstclWidthList, self.obstclHeightList, self.obstclCoordsList)
			self.multiStep(steps, 0)

			# Write the Coverage as an output
			with open("CoverageOutput.txt","a") as f:
				f.write("%s, %s \n" % (self.numdrones, str(self.coverage(self.drones[0].getComRange())) ))

if __name__ == "__main__":
	dapp = DisplayApp(800, 600)
	dapp.main()
