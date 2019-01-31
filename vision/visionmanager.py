from cameramanager import CameraManager			#see cameramanager.py
from networktables import NetworkTables
import time

def give_script(mode):
        if mode == "lines":
                return "./openmv/lines.py"
        elif mode == "blobs":
                return "./openmv/blobs.py"
        elif mode == "video":
                return "./openmv/video.py"
                
def set_mode(cam, mode):
        script = ""
        with open(give_script(mode), 'r') as fin:
                script = fin.read()
        print(script)
        cam.stop_script()
        cam.exec_script(script)


#camera initialization
cam0mode = "lines"
cam0 = CameraManager("/dev/ttyACM0")

#networkTables initialization
NetworkTables.initialize()
nt = NetworkTables.getTable("CameraFeedback")

#main loop
cam0frame = 0

set_mode(cam0, cam0mode)
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
                        
                elif cam0mode == "blobs":
                        data = []
                        for blob in cam0.data:
                                data.append(blob["cx"])
                                data.append(blob["cy"])
                                data.append(blob["w"])
                                data.append(blob["h"])
                                data.append(blob["pixels"])
                        nt.putNumberArray("cam_0_blobs", data)
                        nt.putNumberArray("cam_0_lineseg", [])

                elif cam0mode == "video":
                        data = []
                        nt.putNumberArray("cam_0_blobs", data)
                        nt.putNumberArray("cam_0_lineseg", [])
                        
        nt.putString("cam_0_status", "ok")
        nt.putNumber("cam_0_frame", cam0frame)
        newmode = nt.getString("cam_0_mode", cam0mode)
        nt.putNumber("cam_0_width", cam0.width)
        nt.putNumber("cam_0_height", cam0.height)
        if newmode != cam0mode:
                cam0mode = newmode
                set_mode(cam0, cam0mode)


                
