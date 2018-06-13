# Drone Simulator
#
# Selim Hassairi
# June 2018

from .Agent import Agent

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
        return self.x <= coords[0] < (self.x + self.w) and self.y <= coords[1] < (self.y + self.h)

    def getArea(self):
        return self.w * self.h
