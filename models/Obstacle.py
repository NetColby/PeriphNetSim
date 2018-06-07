# Drone Simluator
#
# Selim Hassairi
# June 2018

OBSTCL 	     = "#3e4c3a"
OBSTCLBORDER = "#255915"

from .Area import Area


class Obstacle(Area):
    # target area class
    def __init__(self, x=9999, y=9999, w=0, h=0, canvas=None):
        Area.__init__(self,x,y,w,h, canvas)

        self.rect = self.canvas.create_rectangle(
            x-(w/2),y+(h/2),x+(w/2),y-(h/2),
            outline = OBSTCLBORDER, fill = OBSTCL, width= 4)

    # Check if a set of coordinates falls into the Obstacle or not
    def inObstacle(self, x, y) :
       if (x>self.x-(self.w/2) and x<self.x+(self.w/2)) and (y>self.y-(self.h/2) and y<self.y+(self.h/2)):
           print("Agent is in Obstacle")
           return True
       else :
           return False
