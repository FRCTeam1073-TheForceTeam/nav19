import time
import math

class localizer:
    """This class implements localization logic"""
    mFieldMap = None
   
    def __init__(self, fieldMap):
        mFieldMap = fieldMap
            return

    def calculateFieldPosition(self, scanFeatures, odometry, lastPostion):
        """calculate current field position based on field features from lidar
        scan, odometry, and last known position"""

        print ("calculateFieldPosition: empty implementation. Scan len : " + str(len(scanFeatures)))

        #TO DO : Write logic and private methods need to calculate field positiong


        return lastPostion #TO DO return caluclated position?]
    