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
import networkx as nx

# # Calculates the connectivity of a graph and return both the k value (k-edge-connected) and whether or not the graph is fully connected
# def connectivityTEST():
# 	# Translate our simulation to a graph
# 	network = nx.Graph()
# 	network.add_nodes_from([1,2,3,4,5])
# 	network.add_edges_from([(1,2),(1,3),(2,3),(3,4),(3,5),(4,5),(1,4),(5,2)])
#
# 	print(network.nodes)
# 	print(network.edges)
#
# 	# Find the k value
# 	kconnected = True
# 	k = 0
# 	while kconnected:
# 		k += 1
# 		kconnected = nx.is_k_edge_connected(network,k)
# 	k-=1
# 	# Find if it is fully connected or not
# 	if k == 0:
# 		print("This Graph is not fully connected")
# 	else:
# 		print("This Graph is k-connected, k = " + str(k))
#
#
# connectivity()




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


with open("TimeStep-VS-Connectivity.txt","a") as f:
	# Find k-edge-connectivity
	f.write("timeStep,connectivity,connected\n")





# If want to control from command line, uncomment the following line
#numdrones = sys.argv[1]

sim = 11
if sim == 0:
	sim = Simulation.Simulation(1200, 750, numdrones, dronesCoordinatesList, numbasestation, basestationCoordinatesList, tareaboolean, tareaWidth, tareaHeight, tareaCoords, obstclboolean, obstclWidth, obstclHeight, obstclCoordinatesList, batteryLevel, moveConsumption, idleConsumption, comList, False)
	sim.main(1, 1000)
else:
	print("################################################################################")
	print("################################################################################")
	print("Simulation Done. Now proceeding to Display")
	print("################################################################################")
	print("################################################################################")
	dapp = Display.DisplayApp(1200, 750, numdrones, dronesCoordinatesList, numbasestation, basestationCoordinatesList, tareaboolean, tareaWidth, tareaHeight, tareaCoords, obstclboolean, obstclWidth, obstclHeight, obstclCoordinatesList, batteryLevel, moveConsumption, idleConsumption, comList, True)
	dapp.main()
