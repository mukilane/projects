import requests
import serial
import time
from subprocess import call

try:
    port = serial.Serial('/dev/ttyUSB0', 9600)
except:
    print "No connection at USB0"
    exit()

while True:
    val = port.readline().rstrip()
    data = val.split(",")
    if len(data) == 3:
        #if data[2] > 4:
            #call(["xdotool", "click", "1"])
        print(data)
    time.sleep(0.3)
