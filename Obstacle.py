# Drone Simluator
#
# Selim Hassairi
# June 2018

OBSTCL 	     = "#3e4c3a"
OBSTCLBORDER = "#255915"

class Obstacle():
    # target area class
    def __init__(self, x=9999, y=9999, w=0, h=0, canvas=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.canvas = canvas
        self.rect = self.canvas.create_rectangle(
            x-(w/2),y+(h/2),x+(w/2),y-(h/2),
            outline = OBSTCLBORDER, fill = OBSTCL, width= 4)

    def getRect(self) :
        return self.rect

    def getTAwidth(self) :
        return self.w

    def getTAheight(self) :
       return self.h

    # Check if a set of coordinates falls into the Obstacle or not
    def inObstacle(self, x, y) :
       if (x>self.x-(self.w/2) and x<self.x+(self.w/2)) and (y>self.y-(self.h/2) and y<self.y+(self.h/2)):
           print("Agent is in Obstacle")
           return True
       else :
           return False
