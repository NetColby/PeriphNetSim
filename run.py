# Drone Simluator
#
# CP Majgaard & Theo Satloff
# January 2018

# Updated by Emmett Burns and Selim Hassairi
#June 2018

from models import Display
from models import Simulation
from InputFileParser import InputFileParser
import sys

filename = "settings.txt"
parser = InputFileParser(filename)
parser.parse()
numdrones, dronesCoordinatesList, numbasestation, basestationCoordinatesList, tareaboolean, tareaWidth, tareaHeight, tareaCoords, obstclboolean, numobstacle, obstclCoordinatesList, obstclWidth, obstclHeight, batteryLevel, moveConsumption, idleConsumption,comModel = parser.getInput()

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

# If want to control from command line, uncomment the following line
#numdrones = sys.argv[1]
sim = Simulation.Simulation(1200, 675, numdrones, dronesCoordinatesList, numbasestation, basestationCoordinatesList, tareaboolean, tareaWidth, tareaHeight, tareaCoords, obstclboolean, obstclWidth, obstclHeight, obstclCoordinatesList, batteryLevel, moveConsumption, idleConsumption, comList, False)
sim.main(1, 200)
# print("####################################################################################")
# print("####################################################################################")
# print("Simulation Done. Now proceeding to Display")
# print("####################################################################################")
# print("####################################################################################")
# dapp = Display.DisplayApp(1200, 675, numdrones, dronesCoordinatesList, numbasestation, basestationCoordinatesList, tareaboolean, tareaWidth, tareaHeight, tareaCoords, obstclboolean, obstclWidth, obstclHeight, obstclCoordinatesList, batteryLevel, moveConsumption, idleConsumption, comList, True)
# dapp.main()
