from abc import ABC, abstractmethod
import math
from ..Drone import Drone
from .replacement_algorithm import ReplacementAlgorithm


class BaseToRechargeAlgorithm(ReplacementAlgorithm) :

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


        # If drone is about to run out of battery, make it go back to recharge
        if moveConsumption * distClosestBaseStation < batteryLevel and moveConsumption * distClosestBaseStation > batteryLevel - 15 and drone.getHeading() == "Free":
            drone.dying(self.drones)
            pass


        if moveConsumption * distClosestBaseStation < batteryLevel and moveConsumption * distClosestBaseStation > batteryLevel - 20 and drone.getHeading() == "Free":
            drone.setHeading("Base")



        # If close to Base Station, give battery back and set headed to Idle
        if distClosestBaseStation < self.rechargeDist and drone.getHeading() == "Base":
            drone.setBatteryLevel(300)
            drone.setHeading("Idle")
            drone.setCommunicating(False)
            drone.setSentDying(False)

        # Keep the drones in the vicinity of the basestation charged
        if distClosestBaseStation < 20 and drone.getHeading() == "Idle":
            drone.setBatteryLevel(300)
            if drone not in bs.getGarage():
                print("added to garage")
                bs.getGarage().append(drone)
