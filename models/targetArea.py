# Drone Simluator
#
# Selim Hassairi
# June 2018

TAREA 	 = "#606060"
TAREABORDER = "#660066"

class targetArea:
    # target area class
    def __init__(self, w, h, canvas):
        self.w = w
        self.h = h
        self.canvas = canvas
        self.rect = self.canvas.create_rectangle(
            450-(w/2),338+(h/2),450+(w/2),338-(h/2),
            outline = TAREABORDER, fill = TAREA, width= 4)

    def getRect(self) :
        return self.rect

    def getTAwidth(self) :
        return self.w

    def getTAheight(self) :
       return self.h
