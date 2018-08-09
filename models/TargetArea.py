# TargetArea Class
#
# Selim Hassairi
# June 2018

# TargetArea Class, child of Area, child of Agent,
# is like an Area object but has a checker to see if an agent is in it


TAREA 	 = "#606060"
TAREABORDER = "#660066"

from .Area import Area


class targetArea(Area):
    # target area class
    def __init__(self, x, y, w, h, canvas=None):
        Area.__init__(self, x, y, w, h, canvas)
        if self.canvas != None:
            self.rect = self.canvas.create_rectangle(
                x-(w/2),y+(h/2),x+(w/2),y-(h/2),
                outline = TAREABORDER, width= 4)

    def getTAwidth(self) :
        return Area.getAwidth(self)

    def getTAheight(self) :
        return Area.getAheight(self)

    def getCoords(self):
        return (self.x,self.y)

    def notInTargetArea(self,x, y):
        if (x>self.x-(self.w/2) and x<self.x+(self.w/2)) and (y>self.y-(self.h/2) and y<self.y+(self.h/2)):
            return False
        else :
            return True
