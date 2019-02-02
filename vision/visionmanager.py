from cameramanager import CameraManager			#see cameramanager.py
from networktables import NetworkTables
import time
import sys
import io
import http.server
import threading
from PIL import Image



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
        cam.enable_fb(True)
        cam.exec_script(script)

#WARNING!!!! Global variable
imgData = io.BytesIO()

class ImageHandler(http.server.BaseHTTPRequestHandler):
        
        def do_GET(self):
                global imgData 
                # Send response status code
                self.send_response(200)
 
                # Send headers
                self.send_header('Content-type','image/jpeg')
                self.end_headers()

                #print("Sending Image.%d" % imgData.tell())
                # Write content as utf-8 data
                self.wfile.write(imgData.getvalue())
                return
        
        # This stops it spewing output all the time.
        def log_message(self, format, *args):
                return

        
#camera initialization
cam0mode = sys.argv[1]
cam0 = CameraManager("/dev/ttyACM0")

#networkTables initialization
NetworkTables.initialize()
nt = NetworkTables.getTable("CameraFeedback")
nt.putString("cam_0_mode", cam0mode)


# create image webserver

server_address = ('127.0.0.1', 8081)
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
                imgData.seek(0)
                image.save(imgData, format = "JPEG")
                imgData.truncate()



