
import time
import math
import numpy
#from rplidar import RPLidar
from networktables import NetworkTables


global XYarray
XYarray = []
global frames
global possiblePositions[]
global visiblePoints[]
class :
    """A frame manager for lidar. This class is responsible for reading lidar data 
    and maintainning a data frame the represents the latest 360 degree view of the field"""

    mLidar = None
    min_frame_len = 120 # based on onbservation, a scan returns between 125 and 135 points
    max_loop = 5 # arbitrary value
   
    def __init__(self, lidarDevice):
            self.mLidar = lidarDevice
            #global lidar 
            #lidar = RPLidar('COM3')
    def graphCreation(self):

    def pointFinding(self):

    def positionFinder(self):

    def trajectory(self):
        


# Simple test
#lidar = RPLidar('COM3')
time.sleep(5)

Scanner = main(lidar)

#position = coordinateFinder.getCurrentPosition(0)
#print ("Position : " + str(position))

lidar.stop()
lidar.stop_motor()
lidar.disconnect()
