# Drone Simluator
#
# CP Majgaard & Theo Satloff
# January 2018

# Updated by Emmett Burns and Selim Hassairi
# June 2018

# Main file of the simualtor that triggers the creation of the simualtion with the given parameters

from models import Display
from models import Simulation
from InputFileParser import InputFileParser
import sys
import networkx as nx


filename = "settings.txt"
parser = InputFileParser(filename)
parser.parse()
numdrones, dronesCoordinatesList, numbasestation, basestationCoordinatesList, tareaboolean, tareaWidth, tareaHeight, tareaCoords, obstclboolean, numobstacle, obstclCoordinatesList, obstclWidth, obstclHeight, batteryLevel, moveConsumption, idleConsumption,comModel, steps = parser.getInput()

#parses and makes comModel into a list
comList = comModel.split(",")

#will not print status message when given this argument
if "-O" not in sys.argv:
	parser.statusMessage()

#only prins the status of the current simulation
if "-Q" in sys.argv:
	quit()

#determines whether or not the GUI should run
gui = True
#interpretes whether or not to run the GUI
if "-W" in sys.argv:
    gui = False


with open("TimeStep-VS-Connectivity.txt","a") as f:
	# Find k-edge-connectivity
	f.write("timeStep,connectivity,numDrones\n")

with open("TimeStep-VS-NetEnergy.txt","a") as f:
	# Find k-edge-connectivity
	f.write("timeStep,netEnergy\n")

with open("TimeStep-VS-4Energies.txt","a") as f:
	# Find k-edge-connectivity
	f.write("timeStep,mov,idle,send,recieve\n")



# If want to control from command line, uncomment the following line
#numdrones = sys.argv[1]

visual	  = True
if visual == False:
	print("################################################################################")
	print("Initialization Done. Now proceeding to the Simulation")
	print("################################################################################")
	sim = Simulation.Simulation(1200, 750, numdrones, dronesCoordinatesList, numbasestation, basestationCoordinatesList, tareaboolean, tareaWidth, tareaHeight, tareaCoords, obstclboolean, obstclWidth, obstclHeight, obstclCoordinatesList, batteryLevel, moveConsumption, idleConsumption, comList, False)
	sim.main(1, steps)
else:
	print("################################################################################")
	print("Initialization Done. Now proceeding to Display")
	print("################################################################################")
	dapp = Display.DisplayApp(1200, 750, numdrones, dronesCoordinatesList, numbasestation, basestationCoordinatesList, tareaboolean, tareaWidth, tareaHeight, tareaCoords, obstclboolean, obstclWidth, obstclHeight, obstclCoordinatesList, batteryLevel, moveConsumption, idleConsumption, comList, True)
	dapp.main()
