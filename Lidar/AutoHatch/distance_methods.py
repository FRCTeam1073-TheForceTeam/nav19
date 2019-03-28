#!/usr/bin/env python3
'''Records scans to a given file in the form of numpy array.
Usage example:

$ ./record_scans.py out.npy'''
import sys
import numpy as np
from rplidar import RPLidar
import time
import math
import scipy
import statistics

degreesAndDistanceArray = []
relaventPoints = []
coordinateArray = []#contains list of xy points
slopeArray = []
lineSlopeArray = []
ceilSlopeArray = []
pointsOnLine = []
finalArray = []
helpfulAngle = 0
ceilSlope = 0

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
    def array_setup(array):
        for i in array:
            if (i[2] <= 0 and i[2] >= 180) or i[3] == 0.0 or i[3] > 3000:
                continue
            else:
                degreesAndDistanceArray.append((i[2], i[3]))
            return degreesAndDistanceArray

    def coordinate_setup(array):
        for i in array:
            if i[0] >= 0 or i[0] <= 90:
                helpfulAngle = 90 - (i[0]-90)
            elif i[0] > 90 or i[0] <= 180:
                helpfulAngle = 180 - i[0]
            else:
                print("error")
                continue   
            x = math.cos(math.radians(helpfulAngle)) * i[1]
            y = math.sin(math.radians(helpfulAngle)) * i[1]
            coordinateArray.append((x,y))
            return coordinateArray
    def better_point_getter(polarArray, pointArray):
        for i in range(len(pointArray)):
            referencePoint = pointArray[i]
            for j in range(len(pointArray)):
                if j == i:
                    continue
                comparisonPoint = pointArray[j]
                slope =(comparisonPoint[1]-referencePoint[1])/(comparisonPoint[0]-referencePoint[0]) 
                slopeArray.append((referencePoint, comparisonPoint, slope, x, y))
        
        for i in slopeArray:
            ceilSlope = math.ceil(i[2])
            ceilSlopeArray.append(ceilSlope)

        lineSlope = statistics.mode(ceilSlopeArray)
            
        for i in slopeArray:
            if i[2] == lineSlope:
                pointsOnLine.append(i)
        for i in range(len(pointsOnLine)):
            referencePoint = pointsOnLine[i]
            for j in range(len(pointsOnLine)):
                if referencePoint == comparisonPoint:
                    continue
                else:
                    distanceBetween = math.sqrt(((comparisonPoint[2]-referencePoint[2])**2) + ((comparisonPoint[3] - referencePoint[3])**2))
                    if coordinateDistance >= 76.2:
                        finalArray = []
                        finalArray.append(comparisonPoint[0])
                        print(finalArray[0])
                        finalArray.append(referencePoint[0])
                        print(finalArray[1])
                        finalArray.append(distanceBetween) 
                        print(finalArray[2])
                        finalArray.append(ceilSlope)
                        print(finalArray[3])
        return finalArray