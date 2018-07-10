# Drone Simluator
#
# CP Majgaard & Theo Satloff
# January 2018
#updated by Emmett Burns & Selim Hassairi
#June 2018

import math
from .BaseStation import BaseStation

class Drone(BaseStation):
    def __init__(self, x, y, algorithmProvider, pt=None, canvas=None, comModel=None, batteryLevel=100.0, moveConsumption=0.9,
    idleConsumption=0.8, sendConsumption=0.2, recieveConsumption=0.1, agentID=9999):
        BaseStation.__init__(self, x, y, algorithmProvider, pt, canvas, comModel, agentID)
        self.batteryLevel = batteryLevel
        self.moves = True
        self.moveConsumption = moveConsumption
        self.idleConsumption = idleConsumption
        self.sendConsumption = sendConsumption
        self.recieveConsumption = recieveConsumption
        self.heading = "Free"
        self.anchor = None

    ##### MESSAGES ######
    def dying(self, drones):
        # print("coords", self.getCoords())
        self.createPackage("Dyingg&" + str(self.getCoords()), destinationAgentID=self.getDistClosestBaseStation(drones)[2].agentID)
        self.heading = "Base"
	#####################


    # Battery
    def setBatteryLevel(self,bl):
        self.batteryLevel = bl

    def get_battery_level(self):
        # return the current battery level of the drone
        return self.batteryLevel

    #Anchor
    def setAnchor(self, coords):
        self.anchor = coords

    def getAnchor(self):
        return self.anchor

    # Move Conusmption
    def getMoveConsumption(self):
        return self.moveConsumption

    def getDistClosestBaseStation(self, drones):
        # For now just first baseStation #####CHANGEEE
        for drone in drones:
            if type(drone) is BaseStation:
                closestBaseStation = drone
        distClosestBaseStation   = ((self.x - closestBaseStation.getCoords()[0])**2 + (self.y - closestBaseStation.getCoords()[1])**2   )**.5
        # print("x,y,dist",self.x, self.y, distClosestBaseStation)
        coordsClosestBaseStation = closestBaseStation.getCoords()
        return distClosestBaseStation, coordsClosestBaseStation, closestBaseStation

    def move(self, x, y):
        # move drone object by unit vector in direction x/y
        if self.canvas is not None:
            self.canvas.move(self.get_pt(), x, y)
        self.set_coords(self.x + x, self.y + y)
        self.batteryLevel -= self.moveConsumption
        self.update_life_state()

    def idle(self):
        self.batteryLevel -= self.idleConsumption
        self.update_life_state()

    def update_life_state(self):
        if self.batteryLevel < 0.5:
            self.dead = True
            if self.canvas is not None:
                self.canvas.itemconfig(self.pt, fill="red")

    def isDead(self):
        return self.dead

    def do_step(self, obstacles, tarea):
        if not self.dead:
            self.algorithm_provider.run(self, obstacles, tarea)
            self.algorithm_provider.updateComNeighbors(self, obstacles)
            self.sendPackages()

    #returns a list of all the pixels in the com range
    def getCoverage(self, rng):
        comRange = set({})
        droneX = int(self.x)
        droneY = int(self.y)
        startingX = int(self.x-(rng))
        startingY = int(self.y-(rng))
        currentX = startingX
        currentY = startingY
        for i in range(rng):
            for j in range(rng):
                if math.hypot(droneX-currentX, droneY-currentY) < rng:
                    comRange.add((currentX, currentY))
                currentY += 1
            currentX += 1
            currentY = startingY
        return comRange

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

    #returns the mean internodal distance
    def meanInternodalDistance(self, neighbors, rng):
        if neighbors:
            distSum = 0
            for drone in neighbors:
                tcoord = drone.get_coords()
                euclidian = math.hypot(self.x-tcoord[0], self.y-tcoord[1])
                distSum += euclidian
            return distSum/len(neighbors)
        else:
            return None

    #calculates individual drones contribution to uniformity
    def droneUniformity(self, drones, rng):
        neighbors = self.getNeighbors(drones, rng)
        total = 0
        numberOfNeighbors = len(neighbors)
        m = self.meanInternodalDistance(neighbors, rng)
        if neighbors:
            for drone in neighbors:
                tcoord = drone.get_coords()
                d = math.hypot(self.x-tcoord[0], self.y-tcoord[1])
                total += (d - m)**2
            output = (total/numberOfNeighbors)**0.5
            return output
        else:
            return 0
