# Drone Simluator
#
# CP Majgaard & Theo Satloff
# January 2018

import getpass
import math
import os
import random
import tkinter.font as tkf
import tkinter as tk
import tkinter.messagebox
import tkinter.simpledialog
import itertools
import time

from .drone import Drone
from .config import Config
from .algorithms.naive_algorithm import NaiveAlgorithm
from .targetArea import targetArea
from .BaseStation import BaseStation

debug = False

FONTCOLOR = "#b2b6b9"
FRAMECOLOR = "#1f1f1f"
BKGCOLOR = "#161616"
TXTBOXCOLOR = '#303030'
BASESTATIONCLR = "#004C99"


# create a class to build and manage the display
class DisplayApp:

	def __init__(self, width, height):

		# create a tk object, which is the root window
		self.root = tk.Tk()
		self.root.configure(background='#161616')

		# width and height of the window
		self.initDx = width
		self.initDy = height

		# set up the geometry for the window
		self.root.geometry( "%dx%d+50+30" % (self.initDx, self.initDy) )

		# set the title of the window
		self.root.title(eval("'Hi %s, have fun using my GUI!' % (getpass.getuser())"))

		# set the maximum size of the window for resizing
		self.root.maxsize( 1200, 675 )


		# set up the application state
		self.drones = [] # list of drones with canvas point
		self.lines = [] # list of lines connecting drones
		self.data = None # will hold the raw data someday.
		self.tareab = False #presence of a target area
		self.tarea = None #target area field
		self.baseClick = None # used to keep track of mouse movement
		self.view_tx = 0
		self.view_ty = 0

		# setup defaul values for variables
		self.droneSize = 10 # set default size to 10 pixels
		self.colorOption = "#F1A9A0"

		self.config = Config()

		# setup the menus
		self.buildMenus()

		# build the controls
		self.buildControls()

		# build the Canvas
		self.buildCanvas()

		# bring the window to the front
		self.root.lift()

		# - do idle events here to get actual canvas size
		self.root.update_idletasks()

		# set up the key bindings
		self.setBindings()


	def buildMenus(self):

		#---- Declare Menu Object ----#
		# create a new menu object
		menu = tk.Menu(self.root)

		# set the root menu to our new menu
		self.root.config(menu = menu)

		# create a variable to hold the individual menus
		menulist = []

		# create a file menu
		filemenu = tk.Menu( menu )
		menu.add_cascade( label = "File", menu = filemenu )
		menulist.append(filemenu)

		# create commands menu
		cmdmenu = tk.Menu( menu )
		menu.add_cascade( label = "Command", menu = cmdmenu )
		menulist.append(cmdmenu)

		#---- Menu Text ----#
		# first sublist is file menu, second is commands menu
		menutext = [ ['Clear		\xE2\x8C\x98N',
					'Quit			\xE2\x8C\x98Q',
					'-' ],
					['Command 1',
					'-',
					'-' ] ]


		#---- Menu Functions ----#
		# first sublist is file menu, second is commands menu
		menucmd = [ [self.clearData,
					self.handleQuit,
					None],
					[self.handleMenuCmd1,
					None,
					None] ]


		#---- Build Menu ----#
		# build the menu elements and callbacks
		for i in range( len( menulist ) ):
			for j in range( len( menutext[i]) ):
				if menutext[i][j] != '-':
					menulist[i].add_command( label = menutext[i][j], command=menucmd[i][j] )
				else:
					menulist[i].add_separator()

	def createRandomDrones(self, event=None):
		num_drones = self.entry1.get()
		for i in range(int(num_drones)):
			self.createRandomDrone()
		return

	def createRandomDrone(self, event=None):
		if not self.tareab :
			x = random.gauss(self.initDx/2, self.initDx/15)
			y = random.gauss(self.initDy/2, self.initDy/15)

		else:
			x = random.randint(450-(self.tarea.getTAwidth()/2), 450+(self.tarea.getTAwidth()/2))
			y = random.randint(338-(self.tarea.getTAheight()/2), 338+(self.tarea.getTAheight()/2))

		self.createDrone(x, y)
		return

	def createDrone(self, x, y, dx=None, algorithm=NaiveAlgorithm, event=None):
		if dx is None:
			dx = self.droneSize/2
		pt = self.canvas.create_oval(x-dx, y-dx, x+dx, y+dx, fill=self.colorOption, outline='')
		drone = Drone(x-self.view_tx, y-self.view_ty, self.canvas, pt, algorithm(self.config, self.drones))
		self.drones.append(drone)

		self.updateDroneView()

		text = "Created a drone at %s x %s!" % (int(x), int(y))
		self.status.set(text)
		return



	def createBaseStation(self, dx=None, algorithm=NaiveAlgorithm, event=None):
		if dx is None:
			dx = self.droneSize/2
		x = int(self.entry5.get())
		y = int(self.entry6.get())

		pt = self.canvas.create_oval(x-dx, y-dx, x+dx, y+dx, fill=BASESTATIONCLR, outline='')
		baseStation = BaseStation(x-self.view_tx, y-self.view_ty, self.canvas, pt)
		self.drones.append(baseStation)

		self.updateDroneView()

		text = "Created a Base Station at %s x %s!" % (int(x), int(y))
		self.status.set(text)
		return



	def createTargetArea(self, event=None):
		self.tareab = True
		w = int(self.entry2.get())
		h = int(self.entry3.get())
		# print("w is " + w + " type " + str(type(w)))
		self.tarea = targetArea(w,h,self.canvas)
		return

	def clearData(self, event=None):
		for drone in self.drones:
			self.canvas.delete(drone.get_pt())
		del self.drones[:]

		for line in self.lines:
			self.canvas.delete(line)
		self.lines = []

		self.canvas.delete(self.tarea.getRect())
		self.tareab = False


		text = "Cleared the screen"
		self.status.set(text)
		print('Cleared the screen')
		return

	def moveDroneUp(self, event=None):
		self.selectedDrone.move(0, -1)
		self.updateDroneView()

	def moveDroneLeft(self, event=None):
		self.selectedDrone.move(-1, 0)
		self.updateDroneView()

	def moveDroneRight(self, event=None):
		self.selectedDrone.move(1, 0)
		self.updateDroneView()

	def moveDroneDown(self, event=None):
		self.selectedDrone.move(0, 1)
		self.updateDroneView()

	def droneStepSingle(self, event=None):
		self.selectedDrone.do_step()
		self.updateDroneView()

	def droneStep(self, event=None):
		for drone in self.drones:
			drone.do_step()
			#print(drone.get_battery_level())
		#print("\n\n")
		self.updateDroneView()

	def multiStep(self, event=None):
	  steps = self.entry4.get()
	  for i in range(int(steps)):
	   self.root.after(125*i, self.droneStep)

	def updateDroneView(self, event=None):
		self.updateStatisticPanel()
		for line in self.lines:
			self.canvas.delete(line)

		self.lines = []

		pairs = list(itertools.combinations(list(range(0, len(self.drones))), r=2))

		for da, db in pairs:
			if not self.drones[da].dead and not self.drones[db].dead:
				acoord = self.drones[da].get_coords()
				bcoord = self.drones[db].get_coords()
				euclidian = math.hypot(acoord[0]-bcoord[0], acoord[1]-bcoord[1])

				if euclidian < self.config.com_range:
					acoordcanvas = self.canvas.coords(self.drones[da].get_pt())
					bcoordcanvas = self.canvas.coords(self.drones[db].get_pt())

					l = self.canvas.create_line(acoordcanvas[0]+self.droneSize/2,
												acoordcanvas[1]+self.droneSize/2,
												bcoordcanvas[0]+self.droneSize/2,
												bcoordcanvas[1]+self.droneSize/2,
												fill="red", dash=(4, 2))
					self.lines.append(l)

	# return the num of alive drones
	def numAliveDrones(self):
		num = 0
		if not self.drones:
			return num
		for drone in self.drones:
			if drone.get_battery_level() > 0:
				num += 1
		return num

	# return the average energy level of the drones
	def avgEnergyLevel(self):
		energy = 0.0
		if not self.drones:
			return energy
		for drone in self.drones:
			if type(drone) != "<class 'models.BaseStation.BaseStation'>" :
				energy += drone.get_battery_level()
		return energy/len(self.drones)

	# update the statistic panel
	def updateStatisticPanel(self, event=None):
		text = "Alive Drones: " + str(self.numAliveDrones())
		self.statAliveDrone.set(text)
		text = "Avg. Energy Level: " + str(round(self.avgEnergyLevel(), 2))
		self.statAvgEnergy.set(text)

	# create the canvas object
	def buildCanvas(self):
		self.canvas = tk.Canvas( self.root, width=self.initDx, height=self.initDy )
		self.canvas.configure(background=FRAMECOLOR, highlightbackground=BKGCOLOR )
		self.canvas.pack( expand=tk.YES, fill=tk.BOTH )
		return

	def getColor(self):
		color = askcolor()
		print(color)

	# build a frame and put controls in it
	def buildControls(self):
		#---- Menu and Menu Item Declarations (ordered) ----#

		#---- Right Panel ----#
		# make a control frame on the right
		rightcntlframe = tk.Frame(self.root)
		rightcntlframe.configure(background=FRAMECOLOR)
		rightcntlframe.pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.Y) # draw the side frame

		#---- Separator for Right Panel ----#
		# make a separator frame
		sep = tk.Frame( self.root, height=self.initDy, width=2, bg=BKGCOLOR)
		sep.pack( side=tk.RIGHT, padx = 2, pady = 2 ) # draw the side frame border

		#---- Creator Region Label ----#
		# use a label to set the size of the right panel
		label = tk.Label( rightcntlframe, text="Random Drone Generator", width=20, fg=FONTCOLOR )
		label.configure(background=FRAMECOLOR)
		label.pack( side=tk.TOP, pady=10 )

		#---- Input Number of Drones ----#
		self.randomDataText = tk.IntVar(None)
		self.entry1 = tk.Entry(rightcntlframe, textvariable = self.randomDataText, width=10, fg=FONTCOLOR)
		self.entry1.insert(0, 1)
		self.entry1.configure(highlightbackground=FRAMECOLOR, background=TXTBOXCOLOR)
		self.entry1.pack(side = tk.TOP) # draw the entry form for number of random points


		#---- Create Random Drone ----#
		createRandomDroneButton = tk.Button( rightcntlframe, text="Create Random Drones", command=self.createRandomDrones)
		createRandomDroneButton.configure(highlightbackground=FRAMECOLOR)
		createRandomDroneButton.pack(side=tk.TOP)


		#---- Base Station Generator ----#
		label = tk.Label( rightcntlframe, text="Base Station Generator", width=20, fg=FONTCOLOR )
		label.configure(background=FRAMECOLOR)
		label.pack( side=tk.TOP, pady=10 )

		#---- Input Area Width and Height ----#
		label = tk.Label( rightcntlframe, text="x,y coords", width=10, fg=FONTCOLOR )
		label.configure(background=FRAMECOLOR)
		label.pack( side=tk.TOP, pady=2 )

		self.areaWidth = tk.IntVar(None)
		self.entry5 = tk.Entry(rightcntlframe, textvariable = self.areaWidth, width=10, fg=FONTCOLOR)
		self.entry5.insert(0, 2)
		self.entry5.configure(highlightbackground=FRAMECOLOR, background=TXTBOXCOLOR)
		self.entry5.pack(side = tk.TOP) # draw the entry form for area width

		self.areaHeight = tk.IntVar(None)
		self.entry6 = tk.Entry(rightcntlframe, textvariable = self.areaHeight, width=10, fg=FONTCOLOR)
		self.entry6.insert(0, 2)
		self.entry6.configure(highlightbackground=FRAMECOLOR, background=TXTBOXCOLOR)
		self.entry6.pack(side = tk.TOP) # draw the entry form for area height


		#---- Spawn the Base Station ----#
		createBaseStationButton = tk.Button( rightcntlframe, text="Generate Base Station", command=self.createBaseStation)
		createBaseStationButton.configure(highlightbackground=FRAMECOLOR)
		createBaseStationButton.pack(side=tk.TOP)










		# use a label to set the size of the right panel
		label = tk.Label( rightcntlframe, text="Target Area Generator", width=20, fg=FONTCOLOR )
		label.configure(background=FRAMECOLOR)
		label.pack( side=tk.TOP, pady=10 )

		#---- Input Area Width and Height ----#
		label = tk.Label( rightcntlframe, text="Width", width=10, fg=FONTCOLOR )
		label.configure(background=FRAMECOLOR)
		label.pack( side=tk.TOP, pady=1 )
		self.areaWidth = tk.IntVar(None)
		self.entry2 = tk.Entry(rightcntlframe, textvariable = self.areaWidth, width=10, fg=FONTCOLOR)
		self.entry2.insert(0, 50)
		self.entry2.configure(highlightbackground=FRAMECOLOR, background=TXTBOXCOLOR)
		self.entry2.pack(side = tk.TOP) # draw the entry form for area width



		label = tk.Label( rightcntlframe, text="Height", width=10, fg=FONTCOLOR )
		label.configure(background=FRAMECOLOR)
		label.pack( side=tk.TOP, pady=1 )
		self.areaHeight = tk.IntVar(None)
		self.entry3 = tk.Entry(rightcntlframe, textvariable = self.areaHeight, width=10, fg=FONTCOLOR)
		self.entry3.insert(0, 50)
		self.entry3.configure(highlightbackground=FRAMECOLOR, background=TXTBOXCOLOR)
		self.entry3.pack(side = tk.TOP) # draw the entry form for area height

		#---- Create Target Area ----#
		createTargetAreaButton = tk.Button( rightcntlframe, text="Create Target Area", command=self.createTargetArea)
		createTargetAreaButton.configure(highlightbackground=FRAMECOLOR)
		createTargetAreaButton.pack(side=tk.TOP)


		#---- Location Modification Label ----#
		# use a label to set the size of the right panel
		label = tk.Label( rightcntlframe, text="Adjust Selected Drone Loc", width=20, fg = FONTCOLOR )
		label.configure(background=FRAMECOLOR)
		label.pack( side=tk.TOP, pady=10 )

		#---- Up ----#
		droneUp = tk.Button( rightcntlframe, text="Move Drone Up", command=self.moveDroneUp )
		droneUp.configure(highlightbackground=FRAMECOLOR)
		droneUp.pack(side=tk.TOP)

		#---- Left ----#
		droneLeft = tk.Button( rightcntlframe, text="Move Drone Left", command=self.moveDroneLeft )
		droneLeft.configure(highlightbackground=FRAMECOLOR)
		droneLeft.pack(side=tk.TOP)

		#---- Down ----#
		droneDown = tk.Button( rightcntlframe, text="Move Drone Down", command=self.moveDroneDown )
		droneDown.configure(highlightbackground=FRAMECOLOR)
		droneDown.pack(side=tk.TOP)

		#---- Right ----#
		droneRight = tk.Button( rightcntlframe, text="Move Drone Right", command=self.moveDroneRight )
		droneRight.configure(highlightbackground=FRAMECOLOR)
		droneRight.pack(side=tk.TOP)

		#---- Run Simulation Label ----#
		# use a label to set the size of the right panel
		label = tk.Label( rightcntlframe, text="Run Simulation", width=20, fg = FONTCOLOR )
		label.configure(background=FRAMECOLOR)
		label.pack( side=tk.TOP, pady=10 )

		#---- Input Number of Steps ----#
		self.randomDataText = tk.IntVar(None)
		self.entry4 = tk.Entry(rightcntlframe, textvariable = self.randomDataText, width=10, fg=FONTCOLOR)
		self.entry4.insert(0, 10)
		self.entry4.configure(highlightbackground=FRAMECOLOR, background=TXTBOXCOLOR)
		self.entry4.pack(side = tk.TOP) # draw the entry form for number of random points
		#---- MultiStep ----#
		droneMultiStepButton = tk.Button( rightcntlframe, text="Step Drones", command=self.multiStep )
		droneMultiStepButton.configure(highlightbackground=FRAMECOLOR)
		droneMultiStepButton.pack(side=tk.TOP)

		#---- Reset Simulation ----#
		# use a label to set the size of the right panel
		label = tk.Label( rightcntlframe, text="Reset Simulation", width=20, fg = FONTCOLOR )
		label.configure(background=FRAMECOLOR)
		label.pack( side=tk.TOP, pady=10 )

		#---- Reset ----#
		droneStepButton = tk.Button( rightcntlframe, text="Reset", command=self.clearData )
		droneStepButton.configure(highlightbackground=FRAMECOLOR)
		droneStepButton.pack(side=tk.TOP)


		#---- Left Panel ----#
		# make a control frame on the right
		leftcntlframe = tk.Frame(self.root)
		leftcntlframe.configure(background=FRAMECOLOR)
		leftcntlframe.pack(side=tk.LEFT, padx=2, pady=2, fill=tk.Y) # draw the side frame

		#---- Separator for Left Panel ----#
		# make a separator frame
		sep = tk.Frame( self.root, height=self.initDy, width=2, bg=BKGCOLOR)
		sep.pack( side=tk.LEFT, padx = 2, pady = 2 ) # draw the side frame border

		#---- Statistic Region Label ----#
		# use a label to set the size of the right panel
		label = tk.Label( leftcntlframe, text="Statistic Panel", width=20, fg=FONTCOLOR )
		label.configure(background=FRAMECOLOR)
		label.pack( side=tk.TOP, pady=10 )

		#---- Alive Drone Count ----#
		# label to display the number of alive drones
		self.statAliveDrone = tk.StringVar()
		text = "Alive Drones: " + str(self.numAliveDrones())
		self.statAliveDrone.set(text)
		label = tk.Label( leftcntlframe, textvariable = self.statAliveDrone, width = 20, fg=FONTCOLOR)
		label.configure(background=FRAMECOLOR)
		label.pack( side=tk.TOP, pady=10 )

		#---- Average Energy Level ----#
		# label to display the number of alive drones
		self.statAvgEnergy = tk.StringVar()
		text = "Avg. Energy Level: " + str(self.avgEnergyLevel())
		self.statAvgEnergy.set(text)
		label = tk.Label( leftcntlframe, textvariable = self.statAvgEnergy, width = 20, fg=FONTCOLOR)
		label.configure(background=FRAMECOLOR)
		label.pack( side=tk.TOP, pady=10 )

		#---- Bottom Frame ----#
		# make a control frame on the right
		bottomframe = tk.Frame(self.root)
		bottomframe.configure(background=FRAMECOLOR)

		bottomframe.pack(side=tk.BOTTOM, padx=2, pady=2, fill=tk.X)

		#---- Separator for Bottom ----#
		# make a separator frame
		sep = tk.Frame( self.root, width=self.initDx, height=2, bg=BKGCOLOR)
		sep.pack( side=tk.BOTTOM, padx = 2, pady = 2)

		self.mouse1coord = tk.StringVar()
		text = 'X-Position: %s	  Y-Position: %s' % ("---", "---")
		self.mouse1coord.set(text)

		coord1 = tk.Label(bottomframe, textvariable = self.mouse1coord, fg = FONTCOLOR)
		coord1.configure(background=FRAMECOLOR)
		coord1.pack(side = tk.LEFT)

		self.status = tk.StringVar()
		text = '---'
		self.status.set(text)

		console = tk.Label(bottomframe, textvariable = self.status, fg = FONTCOLOR)
		console.configure(background=FRAMECOLOR)
		console.pack(side = tk.RIGHT)

		return

	def buildConsole(self):

		#---- Console Item Declarations (ordered) ----#

		#---- Bottom Frame ----#
		# make a control frame on the right
		bottomframe = tk.Frame(self.root)
		bottomframe.pack(side=tk.BOTTOM, padx=2, pady=2, fill=tk.X)

		#---- Separator for Bottom ----#
		# make a separator frame
		sep = tk.Frame( self.root, width=self.initDx, height=2, bd=1, relief=tk.SUNKEN )
		sep.pack( side=tk.BOTTOM, padx = 2, pady = 2, fill=tk.Y)

		#---- Insert Text into Textbox ----#
		self.t = tk.Text(bottomframe, height=10,width=70)
		self.t.insert(tk.END, "print")

		# configure textbox to act like a console
		self.t.config(state=tk.DISABLED) # turn editing of text off
		scroll=tk.Scrollbar(self.t)
		self.t.yview_pickplace("end") # always scroll to the end of the text box
		self.t.configure(yscrollcommand=scroll.set) # activate scroll bar
		self.t.configure(background='grey')

		self.t.pack(side = tk.LEFT)
		return

	def setBindings(self):

		#---- Set bindings	----#
		# bind mouse motions to the canvas
		self.canvas.bind( '<Button-1>', self.handleMouseButton1 )
		self.canvas.bind( '<Control-Button-1>', self.handleMouseButton2 )
		self.canvas.bind( '<B1-Motion>', self.handleMouseButton1Motion )

		# bind command sequences to the root window
		self.root.bind( '<Command-q>', self.handleQuit )
		self.root.bind( '<Command-n>', self.clearData )

	def handleQuit(self, event=None):
		print('Terminating')
		self.root.destroy()

	def handleButton1(self):
		print('handling command button 1')

	def handleButton2(self):
		print('handling command button 3')

	def handleMenuCmd1(self):
		print('handling menu command 1')

	def handleMouseButton1(self, event):
		self.selectedDrone = None

		text = 'X-Position: %s	  Y-Position: %s' % (event.x, event.y) # print the x and y coordinates of the mouseclick in frame
		self.mouse1coord.set(text)

		foundMatch = False
		self.baseClick = (event.x, event.y)
		for drone in self.drones:
			loc = self.canvas.coords(drone.get_pt())
			if (loc[0] <= event.x <= loc[2] and loc[1] <= event.y <= loc[3]):
				coords = drone.get_coords_for_print()
				color = self.canvas.itemcget(drone.get_pt(), "fill")
				self.selectedDrone = drone
				foundMatch = True
				continue

		if foundMatch:
			text = "Found a (%s) color point at %sx%s with coordinates %sx%s" % (color, event.x, event.y, coords[0], coords[1])
			self.status.set(text)
		else:
			text = "No point at %sx%s" % (event.x, event.y)
			self.status.set(text)

		#print('handle mouse button 1: %d %d' % (event.x, event.y))
		self.baseClick = (event.x, event.y)

	def handleMouseButton2(self, event):
		self.createDrone(event.x, event.y)

	# This is called if the first mouse button is being moved
	def handleMouseButton1Motion(self, event):
		# calculate the difference
		diff = ( event.x - self.baseClick[0], event.y - self.baseClick[1] )

		# move every object in canvas based on mouse movement
		for drone in self.drones:
			loc = self.canvas.coords(drone.get_pt())
			self.canvas.coords( drone.get_pt(), loc[0] + diff[0], loc[1] + diff[1], loc[2] + diff[0], loc[3] + diff[1] )

		for line in self.lines:
			loc = self.canvas.coords(line)
			self.canvas.coords(line, loc[0] + diff[0], loc[1] + diff[1], loc[2] + diff[0], loc[3] + diff[1] )

		# update base click
		self.baseClick = ( event.x, event.y )

		#update difference from view center
		self.view_tx += diff[0]
		self.view_ty += diff[1]

		text = 'X-Position: %s	  Y-Position: %s' % (event.x, event.y) # print the x and y coordinates of the mouse motion in frame
		self.mouse1coord.set(text)

		print('handle button1 motion %d %d' % (diff[0], diff[1]))

	# This is called if the right click mouse button is being moved
	def handleMouseButton2Motion(self, event):
		print('handle button2 motion')

	def main(self):
		print('Entering main loop')
		self.root.mainloop()


class Dialog(tk.Toplevel):

	def __init__(self, parent, title = None):

		tk.Toplevel.__init__(self, parent)

		self.transient(parent)

		if title:
			self.title(title)

		self.parent = parent

		self.result = None

		body = tk.Frame(self)
		self.initial_focus = self.body(body)
		body.configure(background=FRAMECOLOR, highlightbackground=BKGCOLOR )

		body.pack(padx=5, pady=5)

		self.buttonbox()

		self.grab_set()

		if not self.initial_focus:
			self.initial_focus = self

		self.protocol("WM_DELETE_WINDOW", self.cancel)

		self.geometry("+%d+%d" % (parent.winfo_rootx()+50, parent.winfo_rooty()+50))

		self.initial_focus.focus_set()

		self.wait_window(self)

	#
	# construction hooks

	def body(self, master):
		# create dialog body.  return widget that should have
		# initial focus.  this method should be overridden

		pass

	def buttonbox(self):
		# add standard button box. override if you don't want the
		# standard buttons

		box = tk.Frame(self)

		w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
		w.pack(side=tk.LEFT, padx=5, pady=5)
		w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
		w.pack(side=tk.LEFT, padx=5, pady=5)

		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)

		box.pack()

	#
	# standard button semantics

	def ok(self, event=None):

		if not self.validate():
			self.initial_focus.focus_set() # put focus back
			return

		self.withdraw()
		self.update_idletasks()

		self.apply()

		self.cancel()

	def cancel(self, event=None):

		# put focus back to the parent window
		self.parent.focus_set()
		self.destroy()

	#
	# command hooks

	def validate(self):

		return 1 # override

	def apply(self):

		pass # override

if __name__ == "__main__":
	dapp = DisplayApp(800, 600)
	dapp.main()
