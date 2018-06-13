# Drone Simluator
#
# Emmett Burns and Selim Hassairi
#June 2018

import getpass
import math
import os
import random
import tkinter.font as tkf
import tkinter as tk
import tkinter.messagebox
import tkinter.simpledialog
import itertools
import time


from .Drone import Drone
from .Config import Config
from .algorithms.naive_algorithm import NaiveAlgorithm
from .algorithms.naive_algorithm_obstcl_avoider import NaiveAlgorithmObstclAvoider
from .TargetArea import targetArea
from .BaseStation import BaseStation
from .Agent import Agent
from .Obstacle import Obstacle

debug = False

FONTCOLOR = "#b2b6b9"
FRAMECOLOR = "#1f1f1f"
BKGCOLOR = "#161616"
TXTBOXCOLOR = '#303030'
BASESTATIONCLR = "#004C99"


# create a class to build and manage the display
class Simulation:

	def __init__(self, numdrones=None,
				dronescoordinatesList=None, numbasestation=None,
				basestationcoordinatesList=None,
				tareaboolean=None, tareaWidth=None, tareaHeight=None, tareaCoords=None,
				obstclboolean=None, obstclWidth=None, obstclHeight=None, obstclCoords=None,
				steps=None, gui=True):

		# width and height of the window
		self.initDx = width
		self.initDy = height

		# set up the application state
		self.drones = [] # list of drones with canvas point
		self.lines = [] # list of lines connecting drones
		self.data = None # will hold the raw data someday.
		if tareaboolean != None:
			self.tareab = tareaboolean
		else:
			self.tareab = False #presence of a target area
		self.tarea = None #target area field

		self.view_tx = 0
		self.view_ty = 0

		self.config = Config()

		# Generating an initial obstacle
		# self.obstacle = Obstacle(canvas=self.canvas) #Obstacle field
		if obstclboolean :
			self.obstacle = Obstacle(obstclCoords[0],obstclCoords[1],obstclWidth, obstclHeight, canvas=self.canvas)
		else :
			self.obstacle = Obstacle(0,0,0,0, canvas=self.canvas)

		# set up the key bindings
		self.setBindings()

		#field to keep track of how often to print statusMessages
		self.iterations = 0

		#holds the command line arguments from run.py
		self.args = []

		#holds the initial starting statistics to be added to the output file
		self.initialOuput = ""

		#holds whether or not to print to an output file
		self.output = False

		#field that holds whether or not to run the simulation without the GUI
		self.gui = gui

		#hold the number of steps to be used when the runWithoutGUI method is used
		self.steps = None
		if not gui:
			self.steps = steps


		#fields from input file
		self.inputDrones = numdrones
		self.inputDroneCoords = dronescoordinatesList
		self.inputBaaseStations = numbasestation
		self.inputBaseStationCoords = basestationcoordinatesList
		self.inputTargetAreaBoolean = tareaboolean
		self.inputTargetWidth = tareaWidth
		self.inputTargetHeight = tareaHeight
		self.inputTargetCoords = tareaCoords
		self.inputObsctlAreaBoolean = obstclboolean
		self.inputObsctlWidth = obstclWidth
		self.inputObsctlHeight = obstclHeight
		self.inputObsctlCoords = obstclCoords
		self.inputSteps = steps

		#Set up and run the simulation from the file settings
		if numdrones != None and self.gui:
			self.setUpSimulation(numdrones, dronescoordinatesList, numbasestation,
				basestationcoordinatesList,
				tareaboolean, tareaWidth, tareaHeight, tareaCoords,
				obstclboolean, obstclWidth, obstclHeight, obstclCoords,
				steps )


	# Set up and run the simulation from the file settings
	def setUpSimulation(self,numdrones, dronescoordinatesList, numbasestation,
		basestationcoordinatesList,
		tareaboolean, tareaWidth, tareaHeight, tareaCoords,
		obstclboolean, obstclWidth, obstclHeight, obstclCoords,
		steps ) :

		# Target Area Generator
		if tareaboolean :
			self.createTargetArea(x=tareaCoords[0],y=tareaCoords[1],w=tareaWidth, h=tareaHeight)

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

		# Run the simulation
		if self.gui:
			self.multiStep(steps)

	def createRandomDrones(self, event=None):
		num_drones = self.entry1.get()
		for i in range(int(num_drones)):
			self.createRandomDrone()
		return

	def createRandomDrone(self, event=None):
		x = None
		y = None
		print(self.tareab)
		while (x == None and y == None ) or (self.obstacle.inObstacle(x,y)) :
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
		return

	def createDrone(self, x, y, dx=None, algorithm=NaiveAlgorithmObstclAvoider, event=None):
		if dx is None:
			dx = self.droneSize/2
		pt = self.canvas.create_oval(x-dx, y-dx, x+dx, y+dx, fill=self.colorOption, outline='')
		drone = Drone(x-self.view_tx, y-self.view_ty, self.canvas, pt, algorithm(self.config, self.drones))
		self.drones.append(drone)

		self.updateDroneView()

		text = "Created a drone at %s x %s!" % (int(x), int(y))
		self.status.set(text)
		return



	def createBaseStation(self, x=None, y = None, dx=None, algorithm=NaiveAlgorithmObstclAvoider, event=None):
		if dx is None:
			dx = self.droneSize/2
		if x == None and y == None:
			x = int(self.entry5.get())
			y = int(self.entry6.get())

		pt = self.canvas.create_oval(x-3*dx, y-3*dx, x+3*dx, y+3*dx, fill=BASESTATIONCLR, outline='')
		baseStation = BaseStation(x-self.view_tx, y-self.view_ty, self.canvas, pt, algorithm(self.config, self.drones))
		self.drones.append(baseStation)

		self.updateDroneView()

		text = "Created a Base Station at %s x %s!" % (int(x), int(y))
		self.status.set(text)
		return



	def createTargetArea(self, x=450, y=338, w=None, h=None, event=None):
		self.tareab = True
		if w == None and h == None:
			w = int(self.entry2.get())
			h = int(self.entry3.get())
		# print("w is " + w + " type " + str(type(w)))
		self.tarea = targetArea(x,y,w,h,self.canvas)
		return


	def clearData(self, event=None):
		for drone in self.drones:
			self.canvas.delete(drone.get_pt())
		del self.drones[:]

		for line in self.lines:
			self.canvas.delete(line)
		self.lines = []

		if self.tareab:
			self.canvas.delete(self.tarea.getRect())
			self.tareab = False

		self.updateStatisticPanel()
		self.updateDroneView()

		text = "Cleared the screen"
		self.status.set(text)
		#print('Cleared the screen')
		return

	#sorry that this method is a mess
	#this is reponsibe for:
	#putting the drones through one iteration
	#outputting updates to the terminal
	#saving an output file of statistics when necessary
	#returning a tuple to be used for data analysis
	def droneStep(self, event=None, returnStats=False):
		if self.steps == None:
			steps = int(self.entry4.get())
		else:
			steps = self.steps
		frequency = self.interpretFrequency()
		if self.iterations == 0:
			#print(self.statsToOutputFile())
			if self.output:
				self.initialStats = self.statsToOutputFile()
			if frequency != 0:
				self.statusMessage(True)
		for drone in self.drones:
			drone.do_step(self.obstacle)
			#print(drone.get_battery_level())
		self.updateDroneView()

		if frequency != 0:
			if self.iterations%frequency == frequency-1:
				self.statusMessage()
			if frequency == 1 and self.iterations == steps:
				self.statusMessage()
		if self.iterations == steps-1 and self.output:
			self.statsToOutputFile(self.initialStats)
		self.iterations += 1
		if returnStats:
			return (self.avgEnergyLevel(), self.numAliveDrones(), self.numDrones(), self.numBases())


	def multiStep(self, event=None):
		#with GUI
		self.iterations = 0
		if self.steps == None:
			steps = self.entry4.get()
			for i in range(int(steps)):
				self.root.after(125*i, self.droneStep)
		#without GUI
		else:
			#steps = self.steps
			for i in range(self.steps):
				#if statement makes code more efficient by only updating tuple during final iteration
				if i+1 != self.steps:
					self.droneStep()
				else:
					(energy, alive, totalDrones, totalBases) = self.droneStep(None, True)
			return (energy, alive, totalDrones, totalBases)

	# return the num of alive drones
	def numAliveDrones(self):
		num = 0
		if not self.drones:
			return num
		for drone in self.drones:
			if type(drone) is Drone and not drone.isDead():
				num += 1
		return num

	#prints the status of a simulation when in begins
	#set numDrones to True when it becomes necessary to display the number of drones
	def statusMessage(self, numDrones = False):
		if self.iterations == 0:
			print("__________Status Message(after " + str(self.iterations) + " steps)__________")
		else:
			print("__________Status Message(after " + str(self.iterations + 1) + " steps)__________")
		if numDrones:
			print("Running simualation with " + str(self.numAliveDrones()) + " drones.")
		print(str(self.numAliveDrones()) + " drones alive.")
		print("Average Energy Level: " + str(self.avgEnergyLevel()))
		print("Coverage: " + str(self.coverage(105)))
		print("Uniformity: " + str(self.uniformity(105)))
		if(self.numDrones() > 0):
			print("_________Drones_________")
			for agent in self.drones:
				if type(agent) is Drone:
					print("Drone at " + str(agent.get_coords()) + " Alive: " + str(not agent.isDead()))
		if(self.numBases() > 0):
			print("______Base Stations______")
			for agent in self.drones:
				if type(agent) is BaseStation:
					print("Base Station at " + str(agent.get_coords()))
		print("")

	#stores the initial status of the simulation and the writes the starting and final statistics to an output file when given the intiial stats
	def statsToOutputFile(self, initialStats = None):
		stats = ""
		if initialStats == None:
			stats = "__________Before Simulation__________\nTotal Drones:  " + str(self.numDrones()) + "\n"
		else:
			stats = initialStats
			stats += "\n\n__________After Simulation(" + str(self.iterations + 1) +" steps)__________\nTotal Drones:  " + str(self.numDrones()) + "\n"
		stats += "Alive Drones: " + str(self.numAliveDrones()) + "\n"
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

	#runs multiple rapid iterations of the same simulation to gather data
	def runWithoutGUI(self, iterations):
		cumulativeEnergy = 0
		cumulativeAlive = 0
		cumulativeTotalDrones = 0
		cumulativeBases = 0
		for i in range(iterations):
			self.setUpSimulation(self.inputDrones, self.inputDroneCoords, self.inputBaaseStations, self.inputBaseStationCoords, self.inputTargetAreaBoolean, self.inputTargetWidth, self.inputTargetHeight, self.inputSteps)
			(energy, alive, totDrones, totBases) = self.multiStep()
			(cumulativeEnergy, cumulativeAlive, cumulativeTotalDrones, cumulativeBases) = (cumulativeEnergy + energy, cumulativeAlive + alive, cumulativeTotalDrones + totDrones, cumulativeBases + totBases)
			self.clearData()
		avgEnergy = cumulativeEnergy/iterations
		averageAlive = cumulativeAlive/iterations
		avergageTotalDrones = cumulativeTotalDrones/iterations
		averageTotalBases = cumulativeBases/iterations
		output = str(iterations) + " simulations were run with " + "ADD IN LATER" + " drones.\n\n"
		output += "____________Statistics After " + str(self.steps) + " Steps__________\n"
		output += "Average Energy Level: " + str(avgEnergy) + "\nAverage Number of Live Drones: " + str(averageAlive) + "\n"
		output += "Number of Drones: " + str(avergageTotalDrones) + "\nNumber of Base Stations: " + str(averageTotalBases)
		text_file = open("stats_without_GUI.txt", "w")
		text_file.write("%s" % output)
		text_file.close()


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
	def main(self):
		pass

if __name__ == "__main__":
	dapp = DisplayApp(800, 600)
	dapp.main()