# file = open('test_192_144_0',"r")
import sys
import math

class mockLidarIterator:
    """Class read stored lidar data and allow iteration over it"""
    fd = None
    eof = False

    def __init__(self, file):
        self.fd = open(file,"r")
        eof = False

    def __iter__(self):
        return self

    def __next__(self):
        if self.eof == True:
            raise StopIteration

        scan = []

        while(1):
            line = self.fd.readline()
            if not line:
                self.eof = True
                return scan;

            parts = line.strip().split(",")
            scan.append((parts[0],parts[1],parts[2],parts[3]))

            if parts[0] == 'True':
                break
        return scan

def isTowerPairCandidate(reference, compare):
    distance1 = reference[3]
    distance2 = compare[3]
    degrees1 = reference[2]
    degrees2 = compare[2]
    degDelta = min([abs(degrees2 - degrees1),360-abs(degrees2 - degrees1)])
    theta = math.radians(abs(degDelta))
    print(theta)

    # do trig to find distance between points...law of cosines
    distanceBetween = math.sqrt((distance1**2 + distance2**2) - (2*distance1*distance2 * math.cos(theta)))
    print(distanceBetween)

    # a tower will be one of 3 distnaces from the other towers...
    # 4876.8 mm between towers on the same side of the field,
    # 8259.6mm between towers opositive (across the field) from each other,
    # and 9616.1mm to the tower diagonal
    #
    # if the distance between the two input points is one of these values,
    # we mark both as tower candidates
    #
    # we give a +/-500mm tolerance on the check
    if ((distanceBetween >= 4376.8 and distanceBetween <= 5376.8) or
        (distanceBetween >= 7759.6 and distanceBetween <= 8759.6) or
        (distanceBetween >= 9116.1 and distanceBetween <= 10116.1)):
        print("Tower candidate found @: distance :" + str(distance1) + ", degrees :" + str(degrees1))
        return True;

    return False;

def run():
    towercheck(('false',20,298.4,4843.5), ('false',20,53.3,3497.8))


if __name__ == '__main__':
    run()
