import sys
import serial

class CameraManager:

    def findPrompt(self, buffer):
        prompt = bytes(b'>>>')
        pos = buffer.find(prompt)
        if pos < 0:
            return False
        else:
            return True
            
    def waitForPrompt(self):
        counter = 0
        check = b'   '
        while (not self.findPrompt(check) and counter < 10):
            check = self.port.read(1000)
        counter = counter + 1
        
        if counter == 10:
            return False
        else:
            return True
        
        
    def __init__(self, port):
        self.port = serial.Serial(port, baudrate = 230400, timeout=0.1)
        print("serial port open :)")
        self.packetBuffer = bytearray(1000)
        self.readIndex = 0

    def __del__(self):
        self.port.close()

    def init(self, command):
        self.port.write(b'\x03')
        if not self.waitForPrompt():
            return False
    
        self.port.write(b'\x04')
        if not self.waitForPrompt():
            return False

        send = "import %s\r\n" % command 
        self.port.write(send.encode())
        #print(send)
        if not self.waitForPrompt():
            return False

        send = "%s.run()\r\n" % command
       # print(send)
        self.port.write(send.encode())
        return True

    def readLoop(self):
        while (True):
            print(self.port.readline())

    def parseBuffer(self, buffer):
        print("parse buffer " + str(buffer))
        return True

    def processData(self):
        endOfPacket = bytes(b'\r\n')
        view = memoryview(self.packetBuffer);
        bytesRead = self.port.readinto(view[self.readIndex:])
        self.readIndex += bytesRead
        #print(self.readIndex, bytesRead)
        #if bytesRead > 0:
        #    print(bytes(view[0:self.readIndex]))
        parts = self.packetBuffer[0:self.readIndex].partition(endOfPacket)
        #print(parts)
        while len(parts[1]) > 0:
            self.parseBuffer(parts[0])
            view[0:len(parts[2])] = parts[2]
            self.readIndex = len(parts[2])
            parts = self.packetBuffer[0:self.readIndex].partition(endOfPacket)
            


cam = CameraManager("/dev/ttyACM0")
print("CAMERAMANAGER CLASS")
#if cam.init("lines"):
if cam.init("autoColorTrack"):
    print("init okay")
else:
    print("init failed")
    
while True:
    cam.processData()
    #print("loop working")
