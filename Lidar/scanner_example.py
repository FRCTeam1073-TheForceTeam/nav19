import sys
import numpy
from rplidar import RPLidar

PORT_NAME = '/dev/ttyUSB0'


if __name__ == '__main__':

    def run (path):
        '''Main Function'''
        lidar = Lidar(PORT_NAME)
        XYarray = []
        try:
            print('Waaaiiiit for it... Press Crl+C to halt.')
            for scan in lidar.iter_scans():
                data.append(numpy.array(scan))
            except KeyboardInterrupt:
                print ('Trying to stop!')

            lidar.stop()
            lidar.stop_motor()
            lidar.disconnect()
            numpy.save(path, numpy.array(XYarray))
