from models import display
import sys

print(str(sys.argv))


# Variable initialization (relevant)
codelinenum = 0
dronenumber = 0
basestationnumber = 0
xycoordDroneb = True
xycoordBaseStationb = True

# Variable initialization (not relevant)
numdrones = 0
numbasestation = None
steps = 0
tareaboolean=None
tareaWidth=0
tareaHeight=0
dronescoordinatesList = []
basestationcoordinatesList = []

# Reading lines form file
lines = [line.rstrip('\n') for line in open('settings.txt')]

# Parsing and analyzing the input file
for i in range(len(lines)):

    if len(lines[i]) != 0:      #avoiding empty lines

        if lines[i][0] != "#" : #avoiding executing comments
            # print("read  : " + lines[i] )
            codelinenum += 1


            # Checks if we are done with reading coordinates by checking if we reached the steps declaration
            if  lines[i][0] == "n" and codelinenum >= 2:
                    # print("xycoordDroneb = False ")
                    xycoordDroneb = False        #this allows not to execute the following statement

            # Checks if we are done with reading coordinates by checking if we reached the steps declaration
            if  lines[i][0] == "s" :
                    # print("xycoordBaseStationb = False ")
                    xycoordBaseStationb = False        #this allows not to execute the following statement




            ######## check if the following lines are about to be drone coordinates
            if codelinenum >= 2  and xycoordDroneb == True:
                dronenumber += 1

                # Checks for an eventual error if num of coordinates given exceeds the number of drones initally given
                if dronenumber > numdrones :
                    print("ERROR : number of drone coordinates '" + str(dronenumber) + "' cannot exceed number of drones " + str(numdrones))
                    exit()

                # Reads in the coordinates of the drones
                exec("(x"+ str(dronenumber) + ",y" + str(dronenumber) + ",z" + str(dronenumber) + ") = (" + lines[i] + ",0)"  )
                dronescoordinatesList.append(eval("(x"+ str(dronenumber) + ",y" + str(dronenumber) + ",z" + str(dronenumber) + ")"))
                # print("(x"+ str(dronenumber) + ",y" + str(dronenumber) + ") = (" + lines[i] + ")"  )


                if len(lines[i+1]) == 0 : #if next line is no longer coordinates, then xycoordb is False
                    # print("2 xycoordDroneb = False ")
                    xycoordDroneb = False


            ####### check if the following lines are about to be base station coordinates
            if codelinenum >= 3  and xycoordDroneb == False and xycoordBaseStationb == True and numbasestation != None:
                basestationnumber += 1

                # Checks for an eventual error if num of coordinates given exceeds the number of drones initally given
                if basestationnumber > numbasestation :
                    print("ERROR : number of base stations coordinates '" + str(basestationnumber) + "' cannot exceed number of base stations. " + str(numbasestation) )
                    exit()


                # Reads in the coordinates of the base stations
                exec("(x"+ str(basestationnumber) + ",y" + str(basestationnumber) + ",z" + str(basestationnumber) + ") = (" + lines[i] + ",0)"  )
                basestationcoordinatesList.append(eval("(x"+ str(basestationnumber) + ",y" + str(basestationnumber) + ",z" + str(basestationnumber) + ")"))

                if len(lines[i+1]) == 0 : #if next line is no longer coordinates, then xycoordb is False
                    xycoordBaseStationb = False


            ## Else execute the line (declare the variables)
            else :
                exec(lines[i])




# Console messages
print("_____Initial Simulation Settings_____")
print("~ Number of Drones at Start                : " + str(numdrones))
print("~ Some Random Positionning                 : " + str( dronenumber < numdrones ))
print("~ Number of Drones Manually Positionned    : " + str(dronenumber))
print("~ " + str(dronescoordinatesList))

print("~ Number of Base Stations at Start         : " + str(numbasestation))
print("~ Some Random Positionning                 : " + str( basestationnumber < numbasestation ))
print("~ Number of Base St Manually Positionned   : " + str(basestationnumber))
print("~ " + str(basestationcoordinatesList))

print("~ Presence of a Target Area                : " + str(tareaboolean))
if tareaboolean :
    print("~ Dimmensions of Target Area are WxH       : " + str(tareaWidth) + " x " + str(tareaHeight) )
print("~ Running the simulation for a number of   : " + str(steps) + " steps")
print('______________________________________')

#determines whether or not the GUI should run
gui = True
#interpretes whether or not to run the GUI
if "-W" in sys.argv:
    gui = False
            
dapp = display.DisplayApp(1200, 675, numdrones, dronescoordinatesList, numbasestation, basestationcoordinatesList, tareaboolean, tareaWidth, tareaHeight, steps, gui)
# dapp = display.DisplayApp(1200, 675)
dapp.getArgs(sys.argv)
if gui:
    dapp.main()
else:
    dapp.runWithoutGUI(10)
