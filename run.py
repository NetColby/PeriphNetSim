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

print(str(sys.argv))



filename = "settings.txt"
parser = InputFileParser(filename)
parser.parse()
numdrones, dronesCoordinatesList, numbasestation, basestationCoordinatesList, tareaboolean, tareaWidth, tareaHeight, tareaCoords, obstclboolean, numobstacle, obstclCoordinatesList, obstclWidth, obstclHeight, comRange, batteryLevel, moveConsumption, idleConsumption = parser.getInput()
parser.statusMessage()


#determines whether or not the GUI should run
gui = True
#interpretes whether or not to run the GUI
if "-W" in sys.argv:
    gui = False

print(comRange)
print(batteryLevel)
print(moveConsumption)
print(idleConsumption)

# dapp = Display.DisplayApp(1000, 1000, 2, [(100, 100), (200, 200)], 1, [(150, 150)], True, 125, 125, (150, 150), True, 2, 2, (125, 125))
sim = Simulation.Simulation(1200, 675, numdrones, dronesCoordinatesList, numbasestation, basestationCoordinatesList, tareaboolean, tareaWidth, tareaHeight, tareaCoords, obstclboolean, obstclWidth, obstclHeight, obstclCoordinatesList, False)
sim.main(1, 100)
print("####################################################################################")
print("####################################################################################")
print("Simulation Done. Now proceeding to Display")
print("####################################################################################")
print("####################################################################################")
dapp = Display.DisplayApp(1200, 675, numdrones, dronesCoordinatesList, numbasestation, basestationCoordinatesList, tareaboolean, tareaWidth, tareaHeight, tareaCoords, obstclboolean, obstclWidth, obstclHeight, obstclCoordinatesList, True)
dapp.main()
