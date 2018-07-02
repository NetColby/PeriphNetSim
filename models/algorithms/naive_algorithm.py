from .algorithm_provider import AlgorithmProvider
import math

class NaiveAlgorithm(AlgorithmProvider):
    # Attempts to move the given drone to a target distance
    # away from the average coordinates of its neighbors (very naive)
    def individualRun(self, drone):
    	if drone.doesMove():
	        target_dist = self.config.com_range - 20
	        min_dist = self.config.com_range - 50

	        neighbors = self.get_drones_within_com_range(drone)

	        if not neighbors:
	            drone.idle()
	            return

	        xdirs = []
	        ydirs = []

	        past_target = []
	        pre_target = []
	        pre_min = []

	        for d in neighbors:
	            if self.get_distance(d, drone) >= target_dist:
	                past_target.append(d)
	            elif self.get_distance(d, drone) < min_dist:
	                pre_min.append(d)
	            else:
	                pre_target.append(d)

	        if pre_min:
	            #Get mean of drones way too close
	            coords = [n.get_coords() for n in pre_min]
	            x = [i[0] for i in coords]
	            y = [i[1] for i in coords]

	            avgx = sum(x)/len(x)
	            avgy = sum(y)/len(y)

	            origin = drone.get_coords()

	            dx = avgx - origin[0]
	            dy = avgy - origin[1]

	            magnitude = math.hypot(dx, dy)

	            xdirs.append(-dx / magnitude)
	            ydirs.append(-dy / magnitude)

	        elif pre_target:
	            #Get mean of drones too close
	            coords = [n.get_coords() for n in pre_target]
	            x = [i[0] for i in coords]
	            y = [i[1] for i in coords]

	            avgx = sum(x)/len(x)
	            avgy = sum(y)/len(y)

	            origin = drone.get_coords()

	            dx = avgx - origin[0]
	            dy = avgy - origin[1]

	            magnitude = math.hypot(dx, dy)

	            xdirs.append(-dx / magnitude)
	            ydirs.append(-dy / magnitude)

	        elif past_target:
	            #Get mean of drones too far
	            coords = [n.get_coords() for n in past_target]
	            x = [i[0] for i in coords]
	            y = [i[1] for i in coords]

	            avgx = sum(x)/len(x)
	            avgy = sum(y)/len(y)

	            origin = drone.get_coords()

	            dx = avgx - origin[0]
	            dy = avgy - origin[1]

	            magnitude = math.hypot(dx, dy)

	            xdirs.append(dx / magnitude)
	            ydirs.append(dy / magnitude)

	        avx = sum(xdirs) / len(xdirs)
	        avy = sum(ydirs) / len(ydirs)

	        magnitude = math.hypot(avx, avy)

	        drone.move(avx/magnitude, avy/magnitude)

    def get_distance(self, d1, d2):
        c1 = d1.get_coords()
        c2 = d2.get_coords()

        return math.hypot(c1[0] - c2[0], c1[1] - c2[1])
