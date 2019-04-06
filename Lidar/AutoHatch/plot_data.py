#!/usr/bin/env python3
'''Records scans to a given file in the form of numpy array.
Usage example:

$ ./record_scans.py out.npy'''
import sys
import numpy as np
from rplidar import RPLidar
import time
from networktables import NetworkTables


#PORT_NAME = '/dev/ttyUSB0'
PORT_NAME = 'COM3'
NetworkTables.initialize("1073Table")
sd = NetworkTables.getTable("1073Table")


def run(path):
    '''Main function'''
    lidar = RPLidar(PORT_NAME)
    time.sleep(3)
    data = []
    try:
        print('Recording measurments... Press Crl+C to stop.')
        for scan in lidar.iter_scans():
            DistanceAndDegreesArray = []
            for j in scan:
                #print("append")
                DistanceAndDegreesArray.append((j[1], j[2])) 
            #print (len(scan))
            sd.putDoubleArray("plot_data", DistanceAndDegreesArray)
            print("sent")            
    except KeyboardInterrupt:
        print('Stoping.')

    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
    np.save(path, np.array(data))

if __name__ == '__main__':
    run(sys.argv[0])
