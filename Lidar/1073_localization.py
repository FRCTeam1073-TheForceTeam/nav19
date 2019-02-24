"""


author: 

"""
LIDAR_DEVICE = 'COM3' #'/dev/cu.SLAB_USBtoUART' #Cam - where is LiDAR, change to COM5 on most Windows Machines, "/dev/ttyUSB0" on Raspberry Pi, Mac, and Ubuntu
import sys
import time
#import networktables
#from networktables import NetworkTables
import numpy as np
from rplidar import RPLidar as Lidar #Cam - import RPLidar
import fieldScanner #Katherine - import the scanner methods
#Table = networktables.NetworkTablesInstance()
#LidarTable = Table.getTable("1073Table")
lidarArray = []


def Odometry(array):
    accelx= 0#LidarTable.getNumber("accelx", 0)
    array.append(accelx)
    accely = 0#LidarTable.getNumber("accely", 0)
    array.append(accely)
    accelz = 0#LidarTable.getNumber("accelz")
    array.append(accelz)
    gyro = 0#LidarTable.getNumber("gyroRawValue", 0)
    print("Odometry complete!")
    return array
#def LidarArray(array):
    
    
def main(path):
        print(__file__ + " start!!")

        lidar = Lidar(LIDAR_DEVICE)
        time.sleep(3)
        data = []
        try:
          
            print('Recording measurments... Press Crl+C to stop.')
            for scan in lidar.iter_scans():
                #TO DO - call feature extract

                #TO DO - call localizer

                #TO DO - publish to network table

                data.append(np.array(scan))
                print(scan)
        except KeyboardInterrupt:
            print('Stoping.')

        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()
        
        return

if __name__ == '__main__':
    main(sys.argv[0])

   
