from rplidar import RPLidar
import time
import math
import numpy as np

class fieldScanner:
    """A frame manager for lidar. This class is responsible for reading lidar data 
    and maintainning a data frame the represents the latest 360 degree view of the field"""

    mLidar = None
   
    def __init__(self, lidarDevice):
            self.mLidar = lidarDevice

    def getCurrentPosition(self,gyro):
        """Returns current position of the robot based on evaluation of a lidar field scan"""
       
        fieldScan = self.getMostRecentFrame()

       #place = self.extractFeatures(fieldScan, 0, 8229.6/2, 7925)

        #return self.calculatePosition(place, gyro)

    def getMostRecentFrame(self):
        """The purpose of this method is to return the latest lidar field scan"""
        
        #  flush any stale data to ensure that we are getting the latest scan
       # self.mLidar.clear_input() 

        # return the first scan from RPLidar that meets minimum length. 
        # RPLidar.iter_scan provides basic frame manageemnt for us
        #for i,recentFrame in enumerate(self.mLidar.iter_scans()):
            #if i >= 2:
                #print(recentFrame)
                #return recentFrame
        
        return 0   
    def extractFeatures(self, latestFieldScan, gyro, lastX, lastY):
        """The purpose of this method is to return the latest lidar field scan"""

        print ("extractFeatures: empty implementation. Scan len : " + str(len(latestFieldScan)))
        for point in latestFieldScan:
        
            fieldPoints = self.pointOnField(point, gyro, lastX, lastY)
            if fieldPoints == True:
                print(point)

        #TO DO : Write logic to analyze the field scan, identify the towers within
        #        the scan, and return tower locations to caller


        return #TO DO what does your data type look like for returning tower positions?
    def pointOnField(self, point, gyro, lastX, lastY):
        #maxX and maxY are the width and length of the field
        maxX = 8229.6 
        maxY = 16459.2
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
    #def readLidar(self, lidar, ):
         #for scan in lidar.iter_scans():
            #print(len(scan))
            #data.append(np.array(scan))


