import time
import math
import numpy


class fieldScanner:
    possibleTower = []
    IdentificationArray = []
    """A frame manager for lidar. This class is responsible for reading lidar data
    and maintainning a data frame the represents the latest 360 degree view of the field"""

   # mLidar = None

    def __init__(self):
           # self.mLidar = lidarDevice
            return

    def pointOnField(self, point, gyro, lastX, lastY):
        #maxX and maxY are the width and length of the field
        maxX = 324
        maxY = 648
        # Xrange and Yrange are the acceptable distance from objects
        # horizontally and vertically along the field to determin whether or not
        # they are inside the field
        Xrange = 0
        Yrange = 0
        inputDegrees = point[1]

       #these detirmine whether the objects are inside the field
        if inputDegrees > 0 and inputDegrees < 90:
            #calculate x
            print("debug 1")
            realDegrees = 90 - inputDegrees
            Xrange = self.calcHypotenuse(realDegrees, maxX - lastX)
            #calculate y
            realDegrees = inputDegrees
            Yrange = self.calcHypotenuse(realDegrees, maxY - lastY )
        if inputDegrees > 90 and inputDegrees < 180:
            #calculate x
            print("debug 2")
            realDegrees = inputDegrees - 90
            Xrange = self.calcHypotenuse(realDegrees, maxX - lastX)
            #calculate y
            realDegrees = 180 - inputDegrees
            Yrange = self.calcHypotenuse(realDegrees, lastY)
        if inputDegrees > 180 and inputDegrees < 270:
            print("debug 3")
            realDegrees = 270 - inputDegrees
            Xrange = self.calcHypotenuse(realDegrees, maxX - lastX)

            realDegrees = inputDegrees - 180
            Yrange = self.calcHypotenuse(realDegrees, lastY)
        if inputDegrees > 270 and inputDegrees < 360:
            print("debug 4")
            # print("DEBUG : "+ str(inputDegrees) + " " + str(point[2]) + "\n")
            realDegrees = inputDegrees - 270
            Xrange = self.calcHypotenuse(realDegrees, maxX - lastX)

            realDegrees = 360 - inputDegrees
            Yrange = self.calcHypotenuse(realDegrees, maxY - lastY)

        if point[2] <= Yrange and point[2] <= Xrange:
            return True

        print("DEBUG:Ignoring object at" + str(inputDegrees) + " " + str(point[2]))
        return False

    def extractFeatures(self, lidarScan, odometry, X, Y):

        """The purpose of this method is to return the latest lidar field scan"""
        #print ("extractFeatures: empty implementation. Scan len : " + str(len(latestFieldScan)))

        #TO DO : Write logic to analyze the field scan, identify the towers within
        #        the scan, and return tower locations to caller
        for j in range(len(lidarScan)):
            currentReferancePoint = lidarScan[j]
            for i in range(len(lidarScan)):
                if i == j:
                    continue
                currentComparisonPoint = lidarScan[i]

                distance1 = currentReferancePoint[3]
                distance2 = currentComparisonPoint[3]
                degrees1 = currentReferancePoint[2]
                degrees2 = currentComparisonPoint[2]
                theta = math.radians(abs(degrees2 - degrees1))

                if distance1 <= distance2:
                    altitude = math.sin(theta)*distance1
                    adjacent = math.cos(theta)*distance1
                    segment = distance2 - adjacent

                else:
                    altitude = math.sin(theta)*distance2
                    adjacent = math.cos(theta)*distance2
                    segment = distance1 - adjacent

                distanceBetween = math.sqrt((segment*segment) + (altitude*altitude))
                print(distanceBetween)
                
                if ((distanceBetween >= 191 and distanceBetween <= 193) or (distanceBetween >= 323 and distanceBetween <= 325)):
                    print("Tower candidate found @: distance :" + str(distance1) + ", degrees :" + str(degrees1))
                    self.possibleTower.append((0,0,currentReferancePoint[2],currentReferancePoint[3]))
                    break
        return self.possibleTower
        #TO DO what does your data type look like for returning tower positions?]
    #def towerIdentification(self, gyro, towerArray, possibleTower, finalArray):

        #for point in towerArray:
            #if gyro > 360:
                #Divisable = floor(gyro/360)
                #gyro = gyro - (360 * Divisable)


            #if gyro < 180:
                #acurateGyro = gyro + 180
            #else:
                #accurateGyro = gyro - 180

            #degrees = point[2]
            #distance = point[3]

            #if degrees >= 0 and degrees < 90:
                #realDegrees = 90 - degrees
                #towerArray.append(realDegrees)
                #realRadians = radians(realDegrees)
                #x = degrees(math.cos(realRadians))*distance
                #y = degrees(math.sin(realRadians))*distance
            #elif degrees >= 90 and degrees < 180:
                #realDegrees = degrees - 90
                #towerArray.append(realDegrees)
                #realRadians = radians(realDegrees)
                #x = degrees(math.cos(realRadians)*distance)
                #y = degrees(-1*(math.sin(realDegrees)*distance))
            #elif degrees >= 180 and degrees < 270:
                #realDegrees = 270 - degrees
                #towerArray.append(realDegrees)
                #realRadians = radians(realDegrees)
                #x = degrees(-1*(math.cos(realRadians)*distance))
                #y = degrees(-1*(math.sin(realRadians)*distance))
            #elif degrees >= 270 and degrees <= 360:
                #realDegrees = degrees - 270
                #towerArray.append(realDegrees)
                #realRadians = radians(realDegrees)
                #x = degrees(-1*(math.cos(realRadians)*distance))
                #y = degrees(math.sin(realRadians)*distance)
            #else:
                #print("error")
                #continue

            # newX = x(math.degrees(math.cos(gyro)) - y(math.degree(math.sin(gyro)))
            # newY = y(math.degrees(math.sin(gyro)) + x(math.degrees(math.sin(gyro)))
            #IdentificationArray.append[(newX, newY)]
        #for i in range(len(IdentificationArray)):
            #point = IdentificationArray[i]
            #if point[0] == 0 and point[1] == 228:
                #towerArray.append[(0, 228)]
            #if point[0] == 0 and point[1] == 552:
                #towerArray.append[(0, 552)]
            #if point[0] == 324 and point[1] == 552:
                #towerArray.append[(324, 552)]
            #if point[0] == 324 and point[1] == 228:
                #towerArray.append[(324, 552)]

    #def robotPosition(self, array):
        
            #realDegrees = array[1[-3]]
            #realRadians = radians(realDegrees) 
            #distance = array[1[3]]
            #degrees = array[1[2]]
            #newArray=[array[1[-1]], array[2[-1]], array[3[-1]], array[4[-1]]]
            #towerPosition = min(newArray)
            #if towerPosition == (0, 228):            
                #if degrees >= 0 and degrees < 90:
                    #print("error")

                #elif degrees >= 90 and degrees < 180:
                    #print("error")
                #elif degrees >= 180 and degrees < 270:
                    #adjacent = degrees(math.cos(realRadians)*distance)
                    #opposite = degrees(math.sin(realRadians)*distance)

                    #finalX = adjacent
                    #finalY = 228 + opposite

                #else:
                    #adjacent = degrees(math.cos(realRadians)*distance)
                    #opposite = degrees(math.sin(realRadians)*distance)

                    #finalX = opposite
                    #finalY = 228 - adjacent
            #if towerPosition == (0, 552):
                #if degrees >= 0 and degrees < 90:
                    #print("error")
                #elif degrees >= 90 and degrees < 180:
                    #adjacent = 
            #finalArray.append[finalX, finalY]
            

            #831fb426526aebd93b1ce482ea1901d963d69ba2

            #there are 16 possible combinations for the tower's position

    def calcHypotenuse(self, theta, adjacent):
        range = adjacent / math.cos(math.radians(theta))
        return range
    def calculatePosition(self,towerList, gyro):
        """Calculates position based on tower location (found by extractFeatures) and gyro data
            (convert robot perspective to a global field coordinate)"""

        print ("calculatePostion: empty implementation")

        #TO DO : Take tower location data (returned from extractFeatures) and
        #        gyro data and produce a field coordinate location

        return {'x': 0,'y':0}
