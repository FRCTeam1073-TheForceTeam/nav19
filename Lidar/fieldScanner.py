import time
import math


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

        return self.possibleTower
        #TO DO what does your data type look like for returning tower positions?]
    def towerIdentification(self, gyro, towerArray, possibleTower):

        for point in towerArray:
            if gyro > 360:
                Divisable = floor(gyro/360)
                gyro = gyro - (360 * Divisable)


            if gyro < 180:
                acurateGyro = gyro + 180
            else:
                accurateGyro = gyro - 180

            degrees = point[2]
            distance = point[3]

            if degrees >= 0 and degrees < 90:
                realDegrees = 90 - degrees
                possibleTower.append(realDegrees)
                x = math.cos(realDegrees)*distance
                y = math.sin(realDegrees)*distance
            elif degrees >= 90 and degrees < 180:
                realDegrees = degrees - 90
                possibleTower.append(realDegrees)
                x = math.cos(realDegrees)*distance
                y = -1*(math.sin(realDegrees)*distance)
            elif degrees >= 180 and degrees < 270:
                realDegrees = 270 - degrees
                possibleTower.append(realDegrees)
                x = -1*(math.cos(realDegrees)*distance)
                y = -1*(math.sin(realDegrees)*distance)
            elif degrees >= 270 and degrees <= 360:
                realDegrees = degrees - 270
                possibleTower.append(realDegrees)
                x = -1*(math.cos(realDegrees)*distance)
                y = math.sin(realDegrees)*distance
            else:
                print("error")
                continue

            # newX = x(math.degrees(math.cos(gyro)) - y(math.degree(math.sin(gyro)))
            # newY = y(math.degrees(math.sin(gyro)) + x(math.degrees(math.sin(gyro)))
            IdentificationArray.append[(newX, newY)]
        for i in range(len(IdentificationArray)):
            point = IdentificationArray[i]
            if point[0] == 0 and point[1] == 228:
                possibleTower.append[1]
            if point[0] == 0 and point[1] == 552:
                possibleTower.append[2]
            if point[0] == 324 and point[1] == 552:
                possibleTower.append[3]
            if point[0] == 324 and point[1] == 228:
                possibleTower.append[4]

    def robotPosition(self, array):
        for i in array:
            realDegrees = i[-2]
            distance = i[3]
            degrees = i[2]
            if i[-1] == 1:
                towerPosition = (0, 228)
            elif i[-1] == 2:
                towerPosition = (0, 552)
            elif i[-1] == 3:
                towerPosition = (324, 228)
            elif i[-1] == 4:
                towerPosition = (324, 552)
            else:
                print("Bad Data")
                continue

            if degrees >= 0 and degrees < 90:
                quadrant = 1
            elif degrees >= 90 and degrees < 180:
                quadrant = 2
            elif degrees >= 180 and degrees < 270:
                quadrant = 3
            else:
                quadrant = 4

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
