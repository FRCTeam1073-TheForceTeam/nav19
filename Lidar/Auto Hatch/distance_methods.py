#!/usr/bin/env python3
'''Records scans to a given file in the form of numpy array.
Usage example:

$ ./record_scans.py out.npy'''
import sys
import numpy as np
from rplidar import RPLidar
import time
import math
from networktables import NetworkTables

degreesAndDistanceArray = []
relaventPoints = []
outputArray = []
distance = 0

#PORT_NAME = '/dev/ttyUSB0'
PORT_NAME = 'COM3'
class auto_hatch:

    def point_getter(array):
        #print(str(array))
        for h in array:
            if h[1] > 180 or h[2] == 0.0 or h[2] > 1000:
                continue
            else:
                degreesAndDistanceArray.append((h[1], h[2]))


        for i in range(len(degreesAndDistanceArray)-1):
            point1 = degreesAndDistanceArray[i]
            point2 = degreesAndDistanceArray[i+1]
            degreesBetween = min(abs(point2[0] - point1[0]), 360-abs(point2[0]-point1[0]))
            #can we have the lidar mounted so the first 180 degrees are facing outward?

            distanceBetween = math.sqrt((point1[1]**2 + point2[1]**2) -
            (2*point1[1]*point2[1] * math.cos(math.radians(degreesBetween))))

            if distanceBetween >= 152.6:
                print(point1)
                print(point2)
                print(distanceBetween)
                outputArray.append(point1)
                outputArray.append(point2)
                outputArray.append(distanceBetween)
                break
        return outputArray

    def produceTargetRangeSimple(finalArray):
        point1Dist = finalArray[0][1]
        return point1Dist
        #a = finalArray[2] #distance from point 1 to point 2 in the hatch slot area, Katherine will give.
        #dist1 = finalArray[0][1]
        #dist2 = finalArray[1][1] #distance from LiDAR to point 2, Katherine will also give.
        #ahalf = a/2 #finds the middle of point 1 and 2 in the hatch slot area
        #dega = finalArray[1][0] - finalArray[0][0] #Katherine will give us this value - angle mesured from LiDAR between point 2 and 3.
        #degb =  #uses the law of signs to find angle b
        #degc = 180-(dega+degb)
        #this finds the missing angle,or angle "c", by doing 180-(a+b) = c
        #finalDistance = math.sqrt(((ahalf**2) + (dist**2)-(2(ahalf)*(dist)*(math.degrees(math.cos(math.radians(degc)))))))
        #uses the law of cosign to find the squared distance from LiDAR to ahalf.
        #ROOTED it to isolate the actual, final, totally accurate distance between LiDAR and ahalf. You are so welcome.
        #print(finalDistance)
        #return finalDistance


def run(path):
    '''Main function'''

    NetworkTables.initialize("10.10.73.2")
    sd = NetworkTables.getTable("1073Table")

    lidar = RPLidar(PORT_NAME)
    time.sleep(3)
    data = []

    try:
        print('Recording measurments... Press Crl+C to stop.')
        for scan in lidar.iter_scans():
            points = auto_hatch.point_getter(scan)

            if(len(points) == 3 ):
                distance = auto_hatch.produceTargetRangeSimple(points)
                sd.putNumber("simple distance", distance) 
                print("put distance to network table : " + str(distance))   
            else:
                distance = -1
                sd.putValue("simple distance from hatch:", -1)
                print("put distance to network table : " + str(distance)) 

            data.append(np.array(scan))

    except:
        print('Stoping.')

    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
    np.save(path, np.array(data))

if __name__ == '__main__':
    run(sys.argv[1])
