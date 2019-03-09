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
        while len(possibleTower) < 4:
            for scans in len(lidarScan):
                currentReferancePoint = lidarScan[scans-1]
                for i in len(lidarScan):
                    if scans != 1:
                        currentComparisonPoint = lidarScan[i-1]
                    else:
                        currentComparisonPoint = lidarScan[i]

                    distance1 = currentReferancePoint[3]
                    distance2 = currentComparisonPoint[3]
                    degrees1 = currentReferancePoint[2]
                    degrees2 = currentComparisonPoint[2]
                    usefulDegrees = degrees2 - degrees1

                    if distance1 <= distance2:
                        altitude = math.sin(usefulDegrees)*distance1
                        adjacent = math.cos(usefulDegrees)*distance1
                        short = distance1 - adjacent
                    elif distance1 > distance2:
                        altitude = math.sin(usefulDegrees)*distance2
                        adjacent = math.cos(usefulDegrees)*distance2
                        short = distance2 - adjacent  
                    else:
                        print("error")

                    smallDegrees = math.arctan(short/altitude)
                    distanceBetween = altitude/math.cos(smallDegrees)

                    if distaceBetween == 192 or distanceBetween == 324:
                        possibleTower.append(currentReferancePoint, currentComparisonPoint)
                
            return possibleTower
        #TO DO what does your data type look like for returning tower positions?]
    #def towerIdentification(gyro, towerArray):
        

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

