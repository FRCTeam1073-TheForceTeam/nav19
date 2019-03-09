import time
import math


class fieldScanner:
    possibleTower = []
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
                print(distance1)
                print(distance2)
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
                print(altitude)
                #smallRadians = math.atan(altitde/segment)
                #distanceBetween = segment/math.cos(smallRadians)
                distanceBetween = math.sqrt((segment*segment) + (altitude*altitude))
                
                if distanceBetween == 192 or distanceBetween == 324:
                    self.possibleTower.append(currentReferancePoint, currentComparisonPoint)
        return self.possibleTower
        #TO DO what does your data type look like for returning tower positions?]
    def towerIdentification(self, gyro, towerArray):

        for point in towerArray:
            if gyro < 180:
                acurateGyro = gyro + 180
            elif gyro >= 180:
                accurateGyro = gyro - 180
            else:
                print("error")
                accurateGyro = gyro
            degrees = point[2]
            distance = point[3]

            if degrees >= 0 and degrees < 90:
                realDegrees = 90 - degrees
                x = math.cos(realDegrees)*distance
                y = math.sin(realDegrees)*distance
            elif degrees >= 90 and degrees < 180:
                realDegrees = degrees - 90
                x = math.cos(realDegrees)*distance
                y = -1*(math.sin(realDegrees)*distance)
            elif degrees >= 180 and degrees < 270:
                realDegrees = 270 - degrees
                x = -1*(math.cos(realDegrees)*distance)
                y = -1*(math.sin(realDegrees)*distance)
            elif degrees >= 270 and degrees <= 360:
                realDegrees = degrees - 270
                x = -1*(math.cos(realDegrees)*distance)
                y = math.sin(realDegrees)*distance
            else:
                print("error")
                realDegrees = degrees
            point.append((x,y)) 
            
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

