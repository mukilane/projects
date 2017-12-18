import requests
import serial
import time

url = 'https://maker.ifttt.com/trigger/arduino/with/key/cfSecjPrUxCqVzEB9mqi4x?value1='

try:
	port = serial.Serial('/dev/ttyUSB0', 9600)
except:
	print "No connection at USB0"
	exit()

while True:
	val = port.readline()
	url = url + val;
	try:
		response=requests.get(url)
		print response.content
	except:
		print "Error"
	time.sleep(300)
