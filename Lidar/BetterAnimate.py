#!/usr/bin/env python3
'''Animates distances and measurment quality'''
import sys
from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

PORT_NAME = '/dev/ttyUSB0'
DMAX = 12000
IMIN = 0
IMAX = 50

class mockLidarIterator:
    """Class read stored lidar data from an input file and allows a consumer to
    iterate over it as if it were lidar input"""
    fd = None

    def __init__(self, file):
        self.fd = open(file,"r")

    def __iter__(self):
        return self

    def __next__(self):
        scan = []

        while(1):
            line = self.fd.readline()
            if not line:
                self.fd.seek(0) # reset to beginning of input file
                return scan;

            parts = line.strip().split(",")
            print(parts)
            if len(parts) == 1:
                parts = line.strip().split("\t") # try tab separated
                print(parts)
            scan.append((int(parts[1]),float(parts[2]),float(parts[3])))

            if parts[0] == 'True':
                break
        return scan

def update_line(num, iterator, line):
    scan = next(iterator)
    offsets = np.array([(np.radians(meas[1]), meas[2]) for meas in scan])
    line.set_offsets(offsets)
    intens = np.array([meas[0] for meas in scan])
    line.set_array(intens)
    return line

def runLidar():
    lidar = RPLidar(PORT_NAME)

    iterator = lidar.iter_scans()
    animateDataStream(iterator)
    lidar.stop()
    lidar.disconnect()

def runFromFile(file):
    iterator = mockLidarIterator(file)
    animateDataStream(iterator)

def animateDataStream(iterator):
    fig = plt.figure()
    ax = plt.subplot(111, projection='polar')
    line = ax.scatter([0, 0], [0, 0], s=5, c=[IMIN, IMAX])
    ax.set_rmax(DMAX)
    ax.grid(True)

    ani = animation.FuncAnimation(fig, update_line,
        fargs=(iterator, line), interval=50)
    plt.show()

if __name__ == '__main__':
    args = sys.argv[1:]

    if len(args) > 0:
        if args[0] == "-i":
            runFromFile(args[1])

    else:
        runLidar()
