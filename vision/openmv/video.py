# Hello World Example
#
# Welcome to the OpenMV IDE! Click on the gear button above to run the script!

import sensor, image, time
import pyb

led1 = pyb.LED(1)
led2 = pyb.LED(2)

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565
sensor.set_framesize(sensor.QVGA)  # Set frame size to QVGA (320x240)
led1.on()
sensor.skip_frames(time = 1500)     # Wait for settings take effect.
led1.off()
clock = time.clock()                # Create a clock object to track the FPS.

while(True):
    clock.tick()                    # Update the FPS clock.
    img = sensor.snapshot()         # Take a picture and return the image.
