#!/usr/bin/env python3
'''Records scans to a given file in the form of numpy array.
Usage example:

$ ./record_scans.py out.npy'''
import sys
import numpy as np
from rplidar import RPLidar
import time

degreesAndDistanceArray = []
relaventPoints = []


#PORT_NAME = '/dev/ttyUSB0'
PORT_NAME = 'COM3'
class auto_hatch:

    def find_distance(self, array, outputArray):
        
    def point_getter(self, array):
        for i in array:
            if i[2] > 90 and i[2] < 270 and i[3] == 0.0 and i[3] > 762:
                continue
            else:
                if i[2] > 270:
                   i[2] = i[2] - 270
                if i[2] < 90:
                    i[2] = i[2] + 90
               degreesAndDistanceArray.append((i[2], i[3]))
        

        for i in range(len(degreesAndDistanceArray)-1):
            outputArray = []
            point1 = degreesAndDistanceArray[i]
            point2 = degreesAndDistanceArray[i+1]
            degreesBetween = point2[0] - point1[0]
            #can we have the lidar mounted so the first 180 degrees are facing outward?

            distanceBetween = (math.pow(point1[1],2) + math.pow(point2[1],2)) - ((2*point1[1]*point2[1])*(math.cos(degreesBetween)))
            
            if distanceBetween >= 152.6:
                outputArray.append[point1]
                outputArray.append[point2]
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
