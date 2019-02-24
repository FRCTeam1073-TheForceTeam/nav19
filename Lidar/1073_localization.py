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
lidarArray = []


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
#def LidarArray(array):
    
    
def main(path):
        print(__file__ + " start!!")

        lidar = Lidar(LIDAR_DEVICE)
        data = []
        try:
            print('Recording measurments... Press Crl+C to stop.')
            for scan in lidar.iter_scans():
                data.append(np.array(scan))

        except KeyboardInterrupt:
            print('Stoping.')

        lidar.stop()
        lidar.disconnect()
        np.save(path, np.array(data))

        #lidar.start_motor()
        #for scans in lidar.iter_scans():

            # array.append[(degrees, distance)]

            #TO DO - call feature extract

            #TO DO - call localizer

            #TO DO - publish to network table

            #print("scan number: " + len(scans))
    
       # return

if __name__ == '__main__':
    main(sys.argv[0])

   
