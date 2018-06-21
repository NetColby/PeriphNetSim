from abc import ABC, abstractmethod
import math

class AlgorithmProvider(ABC):

    def __init__(self, drones):
        self.drones = drones
        super().__init__()

    @abstractmethod
    def run(self, drone):
        pass

    def get_drones_within_com_range(self, drone):
        # returns a list of drones within communications range
        dronecoord = drone.get_coords()
        drones_in_range = []
        for t in [i for i in self.drones if not i.dead]:
            tcoord = t.get_coords()
            euclidian = math.hypot(dronecoord[0]-tcoord[0], dronecoord[1]-tcoord[1])

            if drone is not t:
                if t.attemptCommunication(euclidian):
                    drones_in_range.append(t)
                    drone.updateNeighbors(drones_in_range)

        return drones_in_range
