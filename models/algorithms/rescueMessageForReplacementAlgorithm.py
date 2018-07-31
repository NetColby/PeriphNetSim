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

        # Same thing as Base To Recharge Algorithm
        BaseToRechargeAlgorithm.makeDecisions(self, drone, obstacles, tarea, baseStationInfoList)


        # MAIN DIFFERENCE : sending a rescue-me message when have twice enough battery to come back to Base Station
        if moveConsumption * distClosestBaseStation * 2 > batteryLevel and drone.getHeading() == "Free" and not drone.sentDying:

            if drone.getDistClosestBaseStation(self.drones)[2].rescued.get(drone.getAbsID()) == None or self.numReplaces < 0:
                drone.dying(self.drones)
                # 				 		print("one is none: rescuedAbsID", drone.rescued.get(drone.getAbsID()), "numReplaces", self.numReplaces)
            elif drone.getDistClosestBaseStation(self.drones)[2].rescued.get(drone.getAbsID()) < self.numReplaces :
                drone.dying(self.drones)
            #     # 				 		print("replace")
            # else:
            #     # 				 		print("pass")
            #     pass
