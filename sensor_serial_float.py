import datetime
from log import warning, info
import serial
import time

ser = None
initedSerialDevice = None

def init(serialDevice):
	global ser 
	ser = serial.Serial(serialDevice,9600,timeout=2)
	if(not ser.is_open):
		ser.open()
	global initedSerialDevice
	initedSerialDevice = serialDevice

def inited():
	global ser
	return ser and ser.is_open

def read(outputFormat, targetTz):
	if(not inited()):
		warning('Module not initied. Call init(...) first')
		return None
	contentStr = None
	try:
		contentStr = ser.readline()
		if(not contentStr):
			return None
		contentStr = contentStr.strip()
		content = float(contentStr)
		now = datetime.datetime.now(targetTz)
		return (now.strftime(outputFormat), content)
	except Exception as e:
		warning('[sensor_serial_float] Error while reading line from ',initedSerialDevice, contentStr, e)
		return None
