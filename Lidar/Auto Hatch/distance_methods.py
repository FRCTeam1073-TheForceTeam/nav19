#!/usr/bin/env python3
'''Records scans to a given file in the form of numpy array.
Usage example:

$ ./record_scans.py out.npy'''
import sys
import numpy as np
from rplidar import RPLidar
import time

degreesAndDistanceArray = []

#PORT_NAME = '/dev/ttyUSB0'
PORT_NAME = 'COM3'
class auto_hatch:

    def find_distance(self, array):
        
    def find_line(self, array):
        for i in array:
            if i[2] > 90 and i[2] < 270 and i[3] != 0:
                continue
            else:
               degreesAndDistanceArray.append((i[2], i[3]))
         
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
