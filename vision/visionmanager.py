from cameramanager import CameraManager			#see cameramanager.py
from networktables import NetworkTables
import time


#camera initialization
cam0mode = "lines"
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
                if cam0mode == "lines":
                        data = []
                        for line in cam0.data:
                                data.append(line["x1"])
                                data.append(line["y1"])
                                data.append(line["x2"])
                                data.append(line["y2"])
                                data.append(line["magnitude"])
                        nt.putNumberArray("cam_0_lineseg", data)
                        nt.putNumberArray("cam_0_blobs",[])
                        
                elif cam0mode == "autoColorTrack":
                        data = []
                        for blob in cam0.data:
                                data.append(blob["cx"])
                                data.append(blob["cy"])
                                data.append(blob["width"])
                                data.append(blob["height"])
                                data.append(blob["pixels"])
                        nt.putNumberArray("cam_0_blobs", data)
                        nt.putNumberArray("cam_0_lineseg", [])
                        
        nt.putString("cam_0_status", "ok")
        nt.putNumber("cam_0_frame", cam0frame)
        newmode = nt.getString("cam_0_mode", cam0mode)
        nt.putNumber("cam_0_width", cam0.width)
        nt.putNumber("cam_0_height", cam0.height)
        if newmode != cam0mode:
                cam0mode = newmode
                cam0.init(cam0mode)
