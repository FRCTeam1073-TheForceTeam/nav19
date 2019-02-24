"""


author: 

"""
LIDAR_DEVICE = '/dev/cu.SLAB_USBtoUART' #Cam - where is LiDAR, change to COM5 on most Windows Machines, "/dev/ttyUSB0" on Raspberry Pi, Mac, and Ubuntu
import sys
import time
import networktables
from networktables import NetworkTables
from multiprocessing import Process
import numpy as np
import math
import matplotlib.pyplot as plt
from rplidar import RPLidar as Lidar #Cam - import RPLidar
import fieldScanner #Katherine - import the scanner methods
Table = networktables.NetworkTablesInstance()
LidarTable = Table.getTable("1073Table")

def Odometry(array):
    accelx= LidarTable.getNumber("accelx", 0)
    array.append(accelx)
    accely = LidarTable.getNumber("accely", 0)
    array.append(accely)
    accelz = LidarTable.getNumber("accelz")
    array.append(accelz)
    gyro = LidarTable.getNumber("gyroRawValue", 0)
    print("Odometry complete!")
    return array

def LidarArray(array):
    for measurement in lidar.iter_measurments():
        degrees = measurement[2]
        distance = measurement[3]
        array.append[(degrees, distance)]
        print("LidarArray complete")
        return array

#def scan(path):
#
#    '''Main function'''
#    for measurement in lidar.iter_measurments():
#        try:
#            if len(lidarArray) >= 2:
#                Odometry(odometryArray)
#                LidarArray(lidarArray)        
#                fieldScanner.fieldScanner.getMostRecentFrame(fieldScanner)
#                fieldScanner.fieldScanner.getCurrentPosition(fieldScanner, gyro)
#                fieldScanner.fieldScanner.pointOnField(fieldScanner, lidarArray, gyro, lidarArray[-1[1]], lidarArray[-1[2]])
#
#            else:
#                continue
#        except KeyboardInterrupt:
#            print('Stopping.')
#            lidar.stop_motor()
#            lidar.stop()
#            lidar.disconnect()
    
def main(path):
    print(__file__ + " start!!")

    
    return

if __name__ == '__main__':
    main(sys.argv[0])
   
