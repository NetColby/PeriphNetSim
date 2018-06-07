# Drone Simluator
#
# Selim Hassairi
# June 2018

TAREA 	 = "#606060"
TAREABORDER = "#660066"

from .Area import Area


class targetArea(Area):
    # target area class
    def __init__(self, w, h, canvas):
        Area.__init__(self, 450,338,w,h, canvas)
        self.rect = self.canvas.create_rectangle(
            450-(w/2),338+(h/2),450+(w/2),338-(h/2),
            outline = TAREABORDER, fill = TAREA, width= 4)

    def getTAwidth(self) :
        return Area.getAwidth(self)

    def getTAheight(self) :
        return Area.getAheight(self)
