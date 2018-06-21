# Drone Simluator
#
# Selim Hassairi
# June 2018

# {
# numBs:10,
# droenum:10,
# dronecoords:[(1,1),(2,2)]
# (xt,yt):(1,2)
# }





class InputFileParser:
    def __init__(self, filename):
        self.filename = filename
        self.input = {}
        """
        input :
        { numdrones : 10, dronesCoordinatesList : [(x1,y1), (x2,y2)],
          numbasestation : 2, basestationCoordinatesList : [(x1,y1), (x2,y2)],
          steps : 20,
          tareaboolean : True, tareaCoords : (xt,yt),
          tareaWidth : 300, tareaHeight : 400,
          obstclboolean : False, "numobstacle" : None, obstclCoordinatesList : [(xo,yo)],
          obstclWidth : 300, obstclHeight : 400,
        }
        """

    def parse(self):

        ###### Variable initialization (relevant)
        codelinenum = 0

        # Total number
        numdrones = 0
        numbasestation = 0
        numobstacle = 0

        # Individual number
        dronenumber = 0
        basestationnumber = 0
        obstclnumber = 0


        #### Checkers used while parsing
        tempcoordDroneb = True
        tempcoordBaseStationb = False
        tempcoordTarea = False
        tempcoordObstacle = False


        self.input =  { "numdrones" : None, "dronesCoordinatesList" : [],
                  "numbasestation" : None, "basestationCoordinatesList" : [],
                  "steps" : None,
                  "tareaboolean" : False, "tareaCoords" : (0,0),
                  "tareaWidth" : 0, "tareaHeight" : 0,
                  "obstclboolean" : False, "numobstacle" : None,  "obstclCoordinatesList" : [],
                  "obstclWidth" : 0, "obstclHeight" : 0,
                  "comRange" : 0, "batteryLevel" : 0, "moveConsumption" : 0.0, "idleConsumption" : 0.0
                }

        # Reading lines form file
        lines = [line.rstrip('\n') for line in open(self.filename)]

        # Parsing and analyzing the input file
        for i in range(len(lines)):

            if len(lines[i]) != 0:      #avoiding empty lines

                if lines[i][0] != "#" : #avoiding executing comments

                    if lines[i][0] in ["n","l","s","t","o","c","b","m","i"] : # Seperate variable decalrations and coords
                        splitLine = lines[i].split("=")
                        self.input[splitLine[0]] = splitLine[1]
                        # print(self.input)


                    else :      # Processing all coordinates
                        splitLine = lines[i].split(",")

                        if len(splitLine)==2:
                            x = int(splitLine[0])
                            y = int(splitLine[1])
                        else:
                            x = None
                            y = None

                        ######## Changing checkers

                        ########

                        # Drones Part
                        if tempcoordDroneb:
                            if self.input["numbasestation"]  is not None:
                                tempcoordDroneb = False
                                tempcoordBaseStationb = True
                            else :
                                dronenumber += 1
                                # Checks for an eventual error if num of coordinates given exceeds the number of drones initally given
                                if dronenumber > int(self.input["numdrones"]) :
                                    print("ERROR : number of drone coordinates " + str(dronenumber) + " cannot exceed number of drones " + str(self.input["numdrones"]))
                                    exit()
                                self.input.get("dronesCoordinatesList").append((x,y))

                        # Base Station Part
                        if tempcoordBaseStationb:
                            if self.input["steps"] is not None :
                                tempcoordBaseStationb = False
                                tempcoordTarea = True
                            else :
                                basestationnumber += 1
                                # Checks for an eventual error if num of coordinates given exceeds the number of drones initally given
                                if basestationnumber > int(self.input["numbasestation"]) :
                                    print("ERROR : number of base stations coordinates " + str(basestationnumber) + " cannot exceed number of base stations " + str(self.input["numbasestation"]))
                                    exit()
                                self.input["basestationCoordinatesList"].append((x,y))
                            if not tempcoordBaseStationb and (basestationnumber != int(self.input["numbasestation"])):
                                print("ERROR : did not give all Base Station coordinates.")
                                exit()

                        # TArea Part
                        if tempcoordTarea:
                            self.input["tareaCoords"] = (x,y)
                            tempcoordTarea = False
                            tempcoordObstacle = True

                        # Obstacle Part
                        elif tempcoordObstacle:

                            # Last Error check
                            if self.input["obstclWidth"] != 0:
                                tempcoordObstacle = False
                            if not tempcoordObstacle and (obstclnumber != int(self.input["numobstacle"])):
                                print("ERROR : did not give all Obstcale coordinates.")
                                exit()

                            if tempcoordObstacle:
                                obstclnumber += 1
                                self.input["obstclCoordinatesList"].append((x,y))

                            # Checks for an eventual error if num of coordinates given exceeds the number of drones initally given
                            if obstclnumber > int(self.input["numobstacle"]) :
                                print("ERROR : number of obstacle coordinates " + str(obstclnumber) + " cannot exceed number of obstacles " + str(self.input["numobstacle"]))
                                exit()




        # Last Fixes
        self.dronenumber = dronenumber
        self.basestationnumber = basestationnumber
        self.obstclnumber = obstclnumber

        self.input["numdrones"] = int(self.input.get("numdrones"))
        self.input["numbasestation"] = int(self.input.get("numbasestation"))
        self.input["numobstacle"] = int(self.input.get("numobstacle"))
        self.input["steps"] = int(self.input.get("steps"))
        self.input["tareaboolean"] = self.input.get("tareaboolean") == "True"
        self.input["obstclboolean"] = self.input.get("obstclboolean") == "True"
        self.input["comRange"] = int(self.input.get("comRange"))
        self.input["batteryLevel"] = int(self.input.get("batteryLevel"))
        self.input["moveConsumption"] = float(self.input.get("moveConsumption"))
        self.input["idleConsumption"] = float(self.input.get("idleConsumption"))

    def getInput(self):
        numdrones             = self.input.get("numdrones")
        dronesCoordinatesList = self.input.get("dronesCoordinatesList")
        numbasestation = self.input.get("numbasestation")
        basestationCoordinatesList = self.input.get("basestationCoordinatesList")
        tareaboolean = self.input.get("tareaboolean")
        tareaWidth = int(self.input.get("tareaWidth"))
        tareaHeight = int(self.input.get("tareaHeight"))
        tareaCoords = self.input.get("tareaCoords")
        obstclboolean = self.input.get("obstclboolean")
        numobstacle = self.input.get("numobstacle")
        obstclCoordinatesList = self.input.get("obstclCoordinatesList")
        obstclWidth = self.input.get("obstclWidth")
        obstclHeight = self.input.get("obstclHeight")
        comRange = self.input.get("comRange")
        batteryLevel = self.input.get("batteryLevel")
        moveConsumption = self.input.get("moveConsumption")
        idleConsumption = self.input.get("idleConsumption")

        return numdrones, dronesCoordinatesList, numbasestation, basestationCoordinatesList, tareaboolean, tareaWidth, tareaHeight, tareaCoords, obstclboolean, numobstacle, obstclCoordinatesList, obstclWidth, obstclHeight, comRange, batteryLevel, moveConsumption, idleConsumption

    def statusMessage(self):
        # Console messages
        print("_____Initial Simulation Settings_____")
        print("~ Number of Drones at Start                : " + str(self.input["numdrones"]))
        print("~ Some Random Positionning                 : " + str(self.dronenumber < self.input["numdrones"] ))
        print("~ Number of Drones Manually Positionned    : " + str(self.dronenumber))
        print("~ " + str(self.input["dronesCoordinatesList"]))

        print("~ Number of Base Stations at Start         : " + str(self.input["numbasestation"]))
        print("~ Some Random Positionning                 : " + str( self.basestationnumber < self.input["numbasestation"] ))
        print("~ Number of Base St Manually Positionned   : " + str(self.basestationnumber))
        print("~ " + str(self.input["basestationCoordinatesList"]))
        print("   _________________________________")
        print("~ Presence of a Target Area                : " + str(self.input["tareaboolean"]) + " centered at " + str(self.input["tareaCoords"]) )
        if self.input["tareaboolean"] :
            print("~ Dimmensions of Target Area are WxH       : " + str(self.input["tareaWidth"]) + " x " + str(self.input["tareaHeight"]) )

        print("~ Presence of an Obstacle                  : " + str(self.input["obstclboolean"])  )
        if self.input["obstclboolean"]:
            print("~ Number of obstacles                      : " + str(self.input["numobstacle"]) )
            print("~ " + str(self.input["obstclCoordinatesList"]) )
            print("~ Dimmensions of Obstacle are WxH           : " + str(self.input["obstclWidth"]) + " x " + str(self.input["obstclHeight"]) )

        print("~ Running the simulation for a number of        : " + str(self.input["steps"]) + " steps")
        print("~ Communication range of drones and base staions: " + str(self.input["comRange"]))
        print("~ Starting battery level of drones              : " + str(self.input["batteryLevel"]))
        print("~ Amount of energy used during a drone's move   : " + str(self.input["moveConsumption"]))
        print("~ Amount of energy used during a drone's idle   : " + str(self.input["idleConsumption"]))
        print('______________________________________')



def main():
    parser = InputFileParser("settings.txt")
    parser.parse()
    parser.statusMessage()

if __name__  == "__main__" :
    main()
