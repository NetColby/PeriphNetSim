#Emmett Burns
#06/14/18
#Simulation.py

# import getpass
# import math
# import os
import random
# import tkinter.font as tkf
# import tkinter as tk
# import tkinter.messagebox
# import tkinter.simpledialog
# import itertools
# import time


from .Drone import Drone
from .Config import Config
from .algorithms.naive_algorithm import NaiveAlgorithm
from .algorithms.naive_algorithm_obstcl_avoider import NaiveAlgorithmObstclAvoider
from .TargetArea import targetArea
from .BaseStation import BaseStation
from .Agent import Agent
from .Obstacle import Obstacle

# create a class to build and manage the display
class Simulation:

	def __init__(self, width, height, numdrones, dronescoordinatesList, numbasestation,
		basestationcoordinatesList,
		tareaboolean, tareaWidth, tareaHeight, tareaCoords,
		obstclboolean, obstclWidth, obstclHeight, obstclCoords, gui=False):

		# width and height of the window (these are here because they maintain uniform spawning of the drones)
		self.initDx = width
		self.initDy = height

		# set up the application state
		self.drones = [] # list of drones with canvas point
		self.lines = [] # list of lines connecting drones
		self.data = None # will hold the raw data someday.

		# Presence or abscence of T.Area and Obstacle
		self.tareab = False
		self.obstclb = False

		self.view_tx = 0
		self.view_ty = 0

		self.config = Config()

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
		self.obstclWidth = obstclWidth
		self.obstclHeight = obstclHeight
		self.obstclCoords = obstclCoords

		#field that holds whether or not to run the simulation without the GUI
		self.gui = gui

		# self.setUpSimulation(0, [], 0, [], False, 0, 0, (0, 0), True, 0, 0, (0, 0))
		if not gui:
			self.setUpSimulation( numdrones, dronescoordinatesList, numbasestation, basestationcoordinatesList, tareaboolean, tareaWidth, tareaHeight, tareaCoords, obstclboolean, obstclWidth, obstclHeight, obstclCoords)


	# Set up and run the simulation from the file settings
	def setUpSimulation(self, numdrones, dronescoordinatesList, numbasestation,
		basestationcoordinatesList, tareaboolean, tareaWidth, tareaHeight, tareaCoords,
		obstclboolean, obstclWidth, obstclHeight, obstclCoords):

		self.tarea = None
		if tareaboolean :
			self.createTargetArea(tareaCoords[0], tareaCoords[1], tareaWidth, tareaHeight)

		self.obstacle = None
		if obstclboolean:
			self.createObstacle(obstclCoords[0],obstclCoords[1],obstclWidth, obstclHeight)



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

		

	#creates the given number of random drones
	def createRandomDrones(self, numDrones=10):
		for i in range(numDrones):
			self.createRandomDrone()


	#creates and places a drone in a random location
	def createRandomDrone(self, event=None):
		x = None
		y = None
		while (x == None and y == None ) or (self.obstacle.inObstacle(x,y) if self.obstacle!=None else False) :
			if not self.tareab :
				x = random.gauss(self.initDx/2, self.initDx/15)
				y = random.gauss(self.initDy/2, self.initDy/15)

			# Outdated : too spreadout in the T.Area
			# else:
			# 	x = random.randint(450-(self.tarea.getTAwidth()/2), 450+(self.tarea.getTAwidth()/2))
			# 	y = random.randint(338-(self.tarea.getTAheight()/2), 338+(self.tarea.getTAheight()/2))


			else:
				x = random.gauss(self.tarea.getCoords()[0], self.initDx/15)
				while x < self.tarea.getCoords()[0]-(self.tarea.getTAwidth()/2) or x > self.tarea.getCoords()[0]+(self.tarea.getTAwidth()/2):
					x = random.gauss(self.tarea.getCoords()[0], self.initDx/15)

				y = random.gauss( self.tarea.getCoords()[1], self.initDy/15)
				while y < self.tarea.getCoords()[1]-(self.tarea.getTAheight()/2) or y > self.tarea.getCoords()[1]+(self.tarea.getTAheight()/2):
					y = random.gauss(self.tarea.getCoords()[0], self.initDy/15)

		self.createDrone(x, y)

	#creates a drone at the given location
	def createDrone(self, x, y, algorithm=NaiveAlgorithmObstclAvoider, event=None):
		drone = Drone(x-self.view_tx, y-self.view_ty, algorithm(self.config, self.drones))
		self.drones.append(drone)

	#creates a base station at the given location
	def createBaseStation(self, x=100, y = 100, algorithm=NaiveAlgorithmObstclAvoider, event=None):
		baseStation = BaseStation(x-self.view_tx, y-self.view_ty, algorithm(self.config, self.drones))
		self.drones.append(baseStation)

	#creates a target area given x and y coordinates at the target area's center and

	#at this point I begin commenting out line that I would like to remove

	def createTargetArea(self, x=450, y=338, w=None, h=None, event=None):
		self.tareab = True
		# if w == None and h == None:
		# 	w = int(self.entry2.get())def clearData(self, event=None):
		del self.drones[:]
		#self.lines = []

		# if self.tareab:
		# 	self.canvas.delete(self.tarea.getRect())
		# 	self.tareab = False

		# self.updateStatisticPanel()
		# self.updateDroneView()

		# text = "Cleared the screen"
		# self.status.set(text)
		#print('Cleared the screen')
		# return
		# 	h = int(self.entry3.get())
		# print("w is " + w + " type " + str(type(w)))
		self.tarea = targetArea(x, y, w, h)

	def createObstacle(self, x=450, y=338, w=None, h=None, event=None):
		self.obstclb = True
		del self.drones[:]
		self.obstacle = Obstacle(x, y, w, h)

	#resets the simulation
	def clearData(self, event=None):
		del self.drones[:]
		self.lines = []

		if self.tareab:
			self.tareab = False
			self.tarea = None

		if self.obstclb:
			self.obstclb = False
			self.obstacle = None

		print('Simulation has been reset.')

	#updates the location of the drones based on their algorithm
	def droneStep(self):
		# if self.steps == None:
		# 	steps = int(self.entry4.get())
		# else:
		# 	steps = self.steps
		# frequency = self.interpretFrequency()
		# if self.iterations == 0:
		# 	#print(self.statsToOutputFile())
		# 	if self.output:
		# 		self.initialStats = self.statsToOutputFile()
		# 	if frequency != 0:
		# 		self.statusMessage(True)
		for drone in self.drones:
			drone.do_step(self.obstacle)
			#print(drone.get_battery_level())
		# self.updateDroneView()

		# if frequency != 0:
		# 	if self.iterations%frequency == frequency-1:
		# 		self.statusMessage()
		# 	if frequency == 1 and self.iterations == steps:
		# 		self.statusMessage()
		# if self.iterations == steps-1 and self.output:
		# 	self.statsToOutputFile(self.initialStats)
		# self.iterations += 1
		# if returnStats:
		# 	return (self.avgEnergyLevel(), self.numAliveDrones(), self.numDrones(), self.numBases())

	#runs the simulation for the given number of steps and prints status messages to the terminal
	def multiStep(self, steps, frequency, event=None):
		#variable keeps track of the number of steps in the current simulation for printing status messages
		stepsForStatus = 0
		stringForOutputFile = self.statsToOutputFile()
		for i in range(steps):
			if (stepsForStatus % frequency) == 0:
				print(self.statusMessage(stepsForStatus))
			self.droneStep()
			stepsForStatus += 1
		if (stepsForStatus-1 % frequency) != 0:
			print(self.statusMessage(stepsForStatus))
		self.statsToOutputFile(stringForOutputFile, stepsForStatus)


	# return the num of alive drones
	def numAliveDrones(self):
		num = 0
		if self.drones:
			for drone in self.drones:
				if type(drone) is Drone and not drone.isDead():
					num += 1
		return num

	#prints the status of a simulation when in begins
	#set numDrones to True when it becomes necessary to display the number of drones
	def statusMessage(self, stepsForStatus):
		output = "________________________Statistics after " + str(stepsForStatus) + " steps:________________________\n"
		output += str(self.numAliveDrones()) + " drones alive.\n"
		output += "Average Energy Level: " + str(self.avgEnergyLevel()) + "\n"
		# output += "Coverage: " + str(self.coverage(105)) + "\n"
		output += "Uniformity: " + str(self.uniformity(105)) + "\n\n"
		if(self.numDrones() > 0):
			output += "_________Drones_________\n"
			for agent in self.drones:
				if type(agent) is Drone:
					output += "Drone at " + str(agent.get_coords()) + " Alive: " + str(not agent.isDead()) + "\n"
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
			output += "Coordinates of Center: " + str(self.obstacle.get_coords_for_print()) + "\n"
			output += "Width x Height: " + str(self.obstacle.getAwidth()) + " x " + str(self.obstacle.getAheight()) + "\n"
		return output

	#stores the initial status of the simulation and the writes the starting and final statistics to an output file when given the intiial stats
	def statsToOutputFile(self, initialStats = None, stepsForStatus=None):
		stats = ""
		if initialStats == None:
			stats = "__________Before Simulation__________\nTotal Drones:  " + str(self.numDrones()) + "\n"
		else:
			stats = initialStats
			stats += "\n\n__________After Simulation(" + str(stepsForStatus) +" steps)__________\nTotal Drones:  " + str(self.numDrones()) + "\n"
		stats += "Live Drones: " + str(self.numAliveDrones()) + "\n"
		if(self.numDrones() > 0):
			stats += ("\nDrones:\n")
			for agent in self.drones:
				if type(agent) is Drone:
					stats += "Drone at " + str(agent.get_coords()) + " Alive: " + str(not agent.isDead()) + "\n"
		if(self.numBases() > 0):
			stats += "\nBase Stations:\n"
			for agent in self.drones:
				if type(agent) is BaseStation:
					stats += "Base Station at " + str(agent.get_coords()) + "\n"
		if initialStats == None:
			return stats
	#self.initialOuput += stats
		if initialStats != None:
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
				self.tareaCoords, self.obstclboolean, self.obstclWidth, self.obstclHeight, self.obstclCoords)
			self.multiStep(steps, 10)

	#__________________________________Getters and setters to be used in Display.py__________________________________




if __name__ == "__main__":
	dapp = DisplayApp(800, 600)
	dapp.main()
