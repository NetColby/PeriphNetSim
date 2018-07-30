from abc import ABC, abstractmethod
import math
from ..Drone import Drone


class ReplacementAlgorithm(ABC):

	def __init__(self, drones, numReplaces=3):
		self.drones = drones
		self.numReplaces = numReplaces

	def makeDecisions(self, drone, obstacles, tarea, baseStationInfoList):
		pass
