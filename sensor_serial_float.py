import datetime
from log import warning, info
import time
import threading

class SensorSerialFloatReader:
    def __init__(self, serialObj):
        self.currentRead = 0.0
        self.serialObj = serialObj
        self.dorun = True
        if(not self.serialObj.is_open):
            self.serialObj.open()
        self.t1 = threading.Thread(target=self.Task1)
        self.t1.start()

    def Task1(self):
        i = 1
        while self.dorun:
            contentStr = None
            try:
                print(i)
                contentStr = self.serialObj.readline()
                print(contentStr)
                if(not contentStr):
                    continue
                contentStr = contentStr.strip()
                self.currentRead = float(contentStr)
            except Exception as e:
                warning('[sensor_serial_float] Error while reading line',
                        contentStr, e)
                self.currentRead = None
                break

        self.serialObj.close()

    def read(self):
        return self.currentRead

    def stop():
        self.dorun = False
