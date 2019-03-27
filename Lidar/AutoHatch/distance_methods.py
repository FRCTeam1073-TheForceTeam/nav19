#!/usr/bin/env python3
'''Records scans to a given file in the form of numpy array.
Usage example:

$ ./record_scans.py out.npy'''
import sys
import numpy as np
from rplidar import RPLidar
import time
import math

degreesAndDistanceArray = []
relaventPoints = []


#PORT_NAME = '/dev/ttyUSB0'
PORT_NAME = 'COM3'
class auto_hatch:
    def point_getter(array):
        for i in array:
            if (i[2] < 225 and i[2] > 45) or i[3] == 0.0 or i[3] > 1000:
                continue
            else:
                degreesAndDistanceArray.append((i[2], i[3]))
        
        for i in range(len(degreesAndDistanceArray)-1):
            outputArray = []
            point1 = degreesAndDistanceArray[i]
            point2 = degreesAndDistanceArray[i+1]
            degreesBetween = min(abs(point2[0] - point1[0]), 360-abs(point2[0]-point1[0]))
            #can we have the lidar mounted so the first 180 degrees are facing outward?

            distanceBetween = math.sqrt((point1[1]**2 + point2[1]**2) - 
            (2*point1[1]*point2[1] * math.cos(math.radians(degreesBetween))))
            
            if distanceBetween >= 152.6:
                print(point1)
                print(point2)
                outputArray.append(point1)
                outputArray.append(point2)
                return outputArray
    

def run(path):
    '''Main function'''
    lidar = RPLidar(PORT_NAME)
    time.sleep(3)
    data = []
    try:
        print('Recording measurments... Press Crl+C to stop.')
        for scan in lidar.iter_scans():
            print (len(scan))
            data.append(np.array(scan))
    except KeyboardInterrupt:
        print('Stoping.')

    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
    np.save(path, np.array(data))

if __name__ == '__main__':
    run(sys.argv[1])
