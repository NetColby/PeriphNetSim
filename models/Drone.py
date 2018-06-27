# Drone Simluator
#
# CP Majgaard & Theo Satloff
# January 2018
#updated by Emmett Burns & Selim Hassairi
#June 2018

import math
from .BaseStation import BaseStation

class Drone(BaseStation):
    def __init__(self, x, y, algorithmProvider, pt=None, canvas=None, comModel=None, batteryLevel=100.0, moveConsumption=0.9, idleConsumption=0.8):
        BaseStation.__init__(self, x, y, algorithmProvider, pt, canvas, comModel)
        self.battery_level = batteryLevel
        self.moves = True
        self.moveConsumption = moveConsumption
        self.idleConsumption = idleConsumption

    def get_battery_level(self):
        # return the current battery level of the drone
        return self.battery_level

    def move(self, x, y):
        # move drone object by unit vector in direction x/y
        if self.canvas is not None:
            self.canvas.move(self.get_pt(), x, y)
        self.set_coords(self.x + x, self.y + y)
        self.battery_level -= self.moveConsumption
        self.update_life_state()

    def idle(self):
        self.battery_level -= self.idleConsumption
        self.update_life_state()

    def update_life_state(self):
        if self.battery_level < 0.5:
            self.dead = True
            if self.canvas is not None:
                self.canvas.itemconfig(self.pt, fill="red")

    def isDead(self):
        return self.dead

    def do_step(self, obstacles, tarea):
        if not self.dead:
            self.algorithm_provider.run(self, obstacles, tarea)

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
        for t in [i for i in drones if not i.dead and type(i) is Drone]:
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
