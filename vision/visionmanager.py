from cameramanager import CameraManager			#see cameramanager.py
from networktables import NetworkTables
import time


#camera initialization
cam0mode = "autoColorTrack"
cam0 = CameraManager("/dev/ttyACM0")
if cam0.init(cam0mode):					#uses openMV example code
        print("init okay")
else:
	print("init failed")   
 
#networkTables initialization
NetworkTables.initialize()
nt = NetworkTables.getTable("CameraFeedback")

#main loop
cam0frame = 0

while True:
        cam0.processData()
        if len(cam0.data) > 0:
                cam0frame = cam0frame + 1
                print(cam0.data)
                #print("res %d fmt %d" %(cam0.res, cam0.fmt))
        nt.putString("cam_0_status", "ok")
        nt.putNumber("cam_0_frame", cam0frame)
        newmode = nt.getString("cam_0_mode", cam0mode)
        if newmode != cam0mode:
                cam0mode = newmode
                cam0.init(cam0mode)
