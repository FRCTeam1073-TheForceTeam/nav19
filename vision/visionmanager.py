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
        cam.exec_script(script)
        cam.enable_fb(True)


#camera initialization, GLOBAL
cam = []

class ImageHandler(http.server.BaseHTTPRequestHandler):
        
        
        def do_GET(self):
                global cam
                print(self.path)
                try:
                        ci = -1
                        camnum = self.path.partition("?")[0]
                        ci = int(camnum[1])
                        
                        imgData = io.BytesIO()
                        cam[ci].get_image(imgData)
                        self.send_response(200)
        
                        self.send_header('Content-Type','image/jpeg')
                        self.send_header('Content-Length', imgData.tell())
                        self.send_header('Cache Control', 'no-cache')
                        self.end_headers()
                        self.wfile.write(imgData.getvalue())
                        return
                except:
                        return
                
        # This stops it spewing output all the time.
        def log_message(self, format, *args):
                return

# Process arguments and set up multiple cameras in the global cam list:
cam_mode = []
cam_mode.append(sys.argv[1])
cam_mode.append(sys.argv[1])
cam_mode.append(sys.argv[1])

# Create all our camera managers
cam.append(CameraManager("/dev/ttyACM0"))
cam.append(CameraManager("/dev/ttyACM1"))
cam.append(CameraManager("/dev/ttyACM2"))


videoPort = sys.argv[2]

#networkTables initialization
serverIP = sys.argv[3]
NetworkTables.initialize(server=serverIP)
nt = NetworkTables.getTable("CameraFeedback")


# create image webserver running on separate thread:
server_address = ('', int(videoPort))
httpd = http.server.HTTPServer(server_address, ImageHandler)
httpdThread = threading.Thread(target = httpd.serve_forever)
httpdThread.start()
                                 
#main loop
cam_frame = []

for ci in range(0,len(cam)):
        set_mode(cam[ci], cam_mode[ci])
        cam_frame.append(0)
        nt.putString("cam_%d_mode" %ci, cam_mode[ci])
        
while True:
        for ci in range(0,len(cam)):
                cam[ci].processData()
                cam_frame[ci] = cam_frame[ci] + 1
                if len(cam[ci].data) > 0:
                        if cam_mode[ci] == "lines":
                                data = []
                                for line in cam.data:
                                        data.append(line["x1"])
                                        data.append(line["y1"])
                                        data.append(line["x2"])
                                        data.append(line["y2"])
                                        data.append(line["magnitude"])
                                nt.putNumberArray("cam_%d_lineseg" %cam[ci].cam, data)
                                nt.putNumberArray("cam_%d_blobs" %cam[ci].cam, [])
                        
                        elif cam_mode[ci] == "blobs":
                                data = []
                                for blob in cam[ci].data:
                                        data.append(blob["cx"])
                                        data.append(blob["cy"])
                                        data.append(blob["w"])
                                        data.append(blob["h"])
                                        data.append(blob["pixels"])
                                nt.putNumberArray("cam_%d_blobs" %cam[ci].cam, [])
                                nt.putNumberArray("cam_%d_lineseg" %cam[ci].cam, [])
                        
                        elif cam_mode[ci] == "video":
                                data = []
                                nt.putNumberArray("cam_%d_blobs" %cam[ci].cam, [])
                                nt.putNumberArray("cam_%d_lineseg" %cam[ci].cam, [])
        
                        elif cam_mode[ci] == "learncolor":
                                data = []
                                nt.putNumberArray("cam_%d_blobs" %cam[ci].cam, [])
                                nt.putNumberArray("cam_%d_lineseg" %cam[ci].cam, [])
                                
                nt.putString("cam_%d_status" %cam[ci].cam, "ok")
                nt.putNumber("cam_%d_frame" %cam[ci].cam, cam_frame[ci])
                nt.putNumber("cam_%d_width" %cam[ci].cam, cam[ci].width)
                nt.putNumber("cam_%d_height" %cam[ci].cam, cam[ci].height)
        
                newmode = nt.getString("cam_%d_mode" %cam[ci].cam, cam_mode[ci])
                if newmode != cam_mode[ci]:
                        cam_mode[ci] = newmode
                        set_mode(cam[ci], cam_mode[ci])
                

                cam[ci].fb_update()
