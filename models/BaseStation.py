# Drone Simluator
#
# Selim Hassairi
# June 2018

from .drone import Drone

class BaseStation(Drone):
    def __init__(self,x,y,canvas,pt) :
        Drone.__init__(self,x,y,canvas,pt,None)
        self.battery_level = 999999

    def move(self, x, y):
        pass

    def idle(self):
        pass

    def update_life_state(self):
        pass

    def do_step(self):
        pass
