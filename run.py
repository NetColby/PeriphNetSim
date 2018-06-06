from models import display


# Variable initialization (relevant)
codelinenum = 0
dronenumber = 0
xycoordb = True

# Variable initialization (not relevant)
numdrones = 0
steps = 0
tareaboolean=None
tareaWidth=0
tareaHeight=0
coordinatesList = []

# Reading lines form file
lines = [line.rstrip('\n') for line in open('settings.txt')]

# Parsing and analyzing the input file
for i in range(len(lines)):

    if len(lines[i]) != 0:      #avoiding empty lines

        if lines[i][0] != "#" : #avoiding executing comments
            codelinenum += 1

            # Checks if we are done with reading coordinates by checking if we reached the steps declaration
            if  lines[i][0] == "s" :
                    xycoordb = False        #this allows not to execute the following statement


            if codelinenum >= 2  and xycoordb == True:    # check if the following lines are about to be coordinates
                dronenumber += 1

                # Checks for an eventual error if num of coordinates given exceeds the number of drones initally given
                if dronenumber > numdrones :
                    print("ERROR : number of coordinates cannot exceed number of drones. ")
                    exit()

                # Reads in the coordinates of the drones
                exec("(x"+ str(dronenumber) + ",y" + str(dronenumber) + ",z" + str(dronenumber) + ") = (" + lines[i] + ",0)"  )
                coordinatesList.append(eval("(x"+ str(dronenumber) + ",y" + str(dronenumber) + ",z" + str(dronenumber) + ")"))
                # print("(x"+ str(dronenumber) + ",y" + str(dronenumber) + ") = (" + lines[i] + ")"  )


                if len(lines[i+1]) == 0 : #if next line is no longer coordinates, then xycoordb is False
                    xycoordb = False

            else :
                exec(lines[i])




# Console messages
print("_____Initial Simulation Settings_____")
print("~ Number of Drones at Start                : " + str(numdrones))
print("~ Some Random Positionning                 : " + str( dronenumber < numdrones ))
print("~ Number of Drones Manually Positionned    : " + str(dronenumber))
print("~ " + str(coordinatesList))
print("~ Presence of a Target Area                : " + str(tareaboolean))
if tareaboolean :
    print("~ Dimmensions of Target Area are WxH       : " + str(tareaWidth) + " x " + str(tareaHeight) )
print("~ Running the simulation for a number of   : " + str(steps) + " steps")
print('______________________________________')




# dapp = display.DisplayApp(1200, 675, numdrones, coordinatesList, tareaboolean, tareaWidth, tareaHeight)
dapp = display.DisplayApp(1200, 675)
dapp.main()
