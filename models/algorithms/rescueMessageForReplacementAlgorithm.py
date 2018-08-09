# Rescue Message for Replacement Algorithm

# Created by Selim Hassairi
# August 2018


# When a drone is about to run out of battery, it sends a resce message to the base station
# the base station sends a drone from its garage to the location of the dying drone
# the original drone flies back to the closest base station's garage, recharges, and can go replace any drone now



from abc import ABC, abstractmethod
import math
from ..Drone import Drone
from .replacement_algorithm import ReplacementAlgorithm
from .baseToRechargeAlgorithm import BaseToRechargeAlgorithm


class RescueMessageForReplacementAlgorithm(ReplacementAlgorithm) :

    def __init__(self, drones, numReplaces, rechargeDist = 20):
        ReplacementAlgorithm.__init__(self, drones, numReplaces)
        self.rechargeDist = rechargeDist

    def makeDecisions(self, drone, obstacles, tarea, baseStationInfoList):
        # Basic Info
        moveConsumption = drone.getMoveConsumption()
        batteryLevel = drone.get_battery_level()

        # Closest BaseStation Info
        distClosestBaseStation      = baseStationInfoList[0]
        coordsClosestBaseStation    = baseStationInfoList[1]
        bs                          = baseStationInfoList[2]


        # MAIN DIFFERENCE : sending a rescue-me message when have twice enough battery to come back to Base Station
        if moveConsumption * distClosestBaseStation * 2 > batteryLevel and drone.getHeading() == "Free" and not drone.sentDying:

            if drone.getDistClosestBaseStation(self.drones)[2].rescued.get(drone.getAbsID()) == None or self.numReplaces < 0:
                drone.dying(self.drones)
                # 				 		print("one is none: rescuedAbsID", drone.rescued.get(drone.getAbsID()), "numReplaces", self.numReplaces)
            elif drone.getDistClosestBaseStation(self.drones)[2].rescued.get(drone.getAbsID()) < self.numReplaces :
                drone.dying(self.drones)

        # If drone is about to run out of battery, make it go back to recharge
        if moveConsumption * distClosestBaseStation < batteryLevel and moveConsumption * distClosestBaseStation > batteryLevel - 15 and drone.getHeading() == "Free":
            drone.setHeading("Base")
            pass

        # If close to Base Station, give battery back and set headed to Idle
        if distClosestBaseStation < self.rechargeDist and drone.getHeading() == "Base":
            bs.getGarage().append(drone)
            print("added to garage")

            drone.setBatteryLevel(300)
            drone.setHeading("Idle")
            drone.setCommunicating(True)
            # drone.setCommunicating(False)
            drone.setSentDying(False)

        # Keep the drones in the vicinity of the basestation charged
        if distClosestBaseStation < 20 and drone.getHeading() == "Idle":
            drone.setBatteryLevel(300)
