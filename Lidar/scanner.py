import time
import math
import numpy
from RPLidar import rplidar
from networktables import NetworkTables

NetworkTables.initialize('10.10.73.2')
table = NetworkTables.getTable('1073Table')
global XYarray
XYarray = []
global frames
frames = 0

class scan:
    """A frame manager for lidar. This class is responsible for reading lidar data 
    and maintainning a data frame the represents the latest 360 degree view of the field"""

    #mLidar = RPLidar('COM3')
    mLidar = none
    min_frame_len = 120 # based on on observation, a scan returns between 125 and 135 points
    max_loop = 5 # arbitrary value
   
    def __init__(self, lidarDevice):
            self.mLidar = lidarDevice
    def XY(self, distance, degrees):
        radians = math.radians(degrees)
        x = distance*math.cos(radians)
        y = distance*math.sin(radians)
        XYarray.append((x, y))
        return XYarray
    def FrameManager(self, degrees):
        ceilDegrees = math.ceil(degrees)
        if ceilDegrees == 0:
            frames = frames + 1
            return frames
    def main(self, ):
        for measurment in self.mLidar.iter_measures():
            self.XY(measurment[2], measurment[1])
            self.FrameManager(measurment[1])
            print(frames)
            print(XYarray[-1])
            table.putData(frames)
            table.putData(XYarray)
            return XYarray


# Simple test
time.sleep(5)

Scanner = scan(mLidar)

#position = Scanner.getCurrentPosition(0)
#print ("Position : " + str(position))
try:
    Scanner.main()
except KeyboardInterrupt:
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
