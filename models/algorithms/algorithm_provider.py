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
            
            if euclidian < self.drones[0].comRange and drone is not t:
                drones_in_range.append(t)

        return drones_in_range
