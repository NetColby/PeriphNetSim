# Drone Simulator
#
# Selim Hassairi
# June 2018

from .agent import Agent

class Area(Agent):
    # target area class
    def __init__(self, x, y, w, h, canvas):
        Agent.__init__(self, x, y, canvas)
        self.w = w
        self.h = h
        # self.rect = self.canvas.create_rectangle(
        #     x-(w/2),y+(h/2),x+(w/2),y-(h/2),
        #     outline = OBSTCLBORDER, fill = OBSTCL, width= 4)

    def getRect(self) :
        return self.rect

    def getAwidth(self) :
        return self.w

    def getAheight(self) :
       return self.h

    def inArea(self, coords):

        return (self.x - (self.w/2)) <= coords[0] and coords[0] < (self.x + (self.w/2)) and (self.y-(self.h/2)) <= coords[1] and coords[1] < (self.y + (self.h/2))

    def getArea(self):
        return self.w * self.h

