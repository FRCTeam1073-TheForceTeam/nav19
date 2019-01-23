import sys
import serial

def findprompt(buffer):
    prompt = bytes(b'>>>')
    pos = buffer.find(prompt)
    if pos < 0:
        return False
    else:
        return True
            
def WaitForPrompt(port):
    counter = 0
    check = b'   '
    while (not findprompt(check) and counter < 10):
        check = port.read(1000)
        counter = counter + 1
        
    if counter == 10:
        return False
    else:
        return True
        
        
def init(port, command):
    port.write(b'\x03')
    if not WaitForPrompt(port):
        return False
    
    port.write(b'\x04')
    if not WaitForPrompt(port):
        return False

    send = "import %s\r\n" % command 
    port.write(send.encode())
    print(send)
    if not WaitForPrompt(port):
        return False

    send = "%s.run()\r\n" % command
    print(send)
    port.write(send.encode())
    return True



ser = serial.Serial("/dev/ttyACM0", baudrate = 230400, timeout = 0.1)
print("serial port open :)")
if init(ser, "lines"):
    print("init okay")
else:
    print("init failed")
    
while (True):
    print(ser.readline())



