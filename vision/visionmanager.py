from cameramanager import CameraManager			#see cameramanager.py
from networktables import NetworkTables
import time
import sys
import io
# Allows us to send images over HTTP
import http.server
# Allows us to run HTTP server in a separate thread so we can poll camera
import threading
# Allows us to convert camera image to JPEG for HTTP Client
from PIL import Image



def give_script(mode):
        if mode == "lines":
                return "./openmv/lines.py"
        elif mode == "blobs":
                return "./openmv/blobs.py"
        elif mode == "video":
                return "./openmv/video.py"
        elif mode == "learncolor":
                return "./openmv/learncolor.py"
                
def set_mode(cam, mode):
        script = ""
        with open(give_script(mode), 'r') as fin:
                script = fin.read()
        print(script)
        cam.stop_script()
        cam.enable_fb(True)
        cam.exec_script(script)

#WARNING!!!! Global variable needs lock
imgData = io.BytesIO()
imgDataLock = threading.Lock()

class ImageHandler(http.server.BaseHTTPRequestHandler):
        
        def do_GET(self):
                global imgData 
                # Send response status code
                self.send_response(200)
 
                # Send headers
                self.send_header('Content-Type','image/jpeg')
                self.send_header('Content-Length', imgData.tell())
                self.end_headers()

                #print("Sending Image.%d" % imgData.tell())
                # Protect thread access to imgData
                imgDataLock.acquire()
                self.wfile.write(imgData.getvalue())
                imgDataLock.release()
                return
        
        # This stops it spewing output all the time.
        def log_message(self, format, *args):
                return

        
#camera initialization
cam0mode = sys.argv[1]
cam0 = CameraManager("/dev/ttyACM0")

videoPort = sys.argv[2]

#networkTables initialization
serverIP = sys.argv[3]
NetworkTables.initialize(server=serverIP)
nt = NetworkTables.getTable("CameraFeedback")
nt.putString("cam_0_mode", cam0mode)


# create image webserver

server_address = ('', int(videoPort))
httpd = http.server.HTTPServer(server_address, ImageHandler)
httpdThread = threading.Thread(target = httpd.serve_forever)
httpdThread.start()
                                 
#main loop
cam0frame = 0

set_mode(cam0, cam0mode)
while True:
        cam0.processData()
        cam0frame = cam0frame + 1
        if len(cam0.data) > 0:
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
                        nt.putNumberArray("cam_0_blobs", [])
                        nt.putNumberArray("cam_0_lineseg", [])

                elif cam0mode == "learncolor":
                        data = []
                        nt.putNumberArray("cam_0_blobs", [])
                        nt.putNumberArray("cam_0_lineseg", [])
                        
        nt.putString("cam_0_status", "ok")
        nt.putNumber("cam_0_frame", cam0frame)
        nt.putNumber("cam_0_width", cam0.width)
        nt.putNumber("cam_0_height", cam0.height)
        
        newmode = nt.getString("cam_0_mode", cam0mode)
        if newmode != cam0mode:
                cam0mode = newmode
                set_mode(cam0, cam0mode)
                
        fb = cam0.fb_dump()
        if fb != None:
                image = Image.fromarray(fb[2])
                # Protect thread access to imgData
                imgDataLock.acquire()
                imgData.seek(0)
                image.save(imgData, format = "JPEG")
                imgData.truncate()
                imgDataLock.release()



