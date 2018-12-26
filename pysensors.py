#!/usr/bin/python

# Google Spreadsheet DHT Sensor Data-logging Example

# Depends on the 'gspread' package being installed.  If you have pip installed
# execute:
# sudo pip install gspread

# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from __future__ import print_function
import sys
import getopt
import moskito
import json
import pytz
import dht_sensor as dht
import onewire_temp_sensor as ow
import airquality_sensor_serial as aqss
import sensor_serial_float as ssf
import time
import datetime
import influks
from log import warning, info
from config import conf
try:
    import google_spreadsheet as gs
except ImportError:
    warning('google_spreadsheet module cannot be loaded') 
#from oauth2client.client import SignedJwtAssertionCredentials
# targetTz = pytz.timezone('Europe/Warsaw')
targetTz = pytz.timezone('UTC')
output_fmt = '%Y-%m-%dT%H:%M:%SZ'
client = moskito.start_client()
i=0
#mqtt_topic_temp=conf['mqtt']['topic_temp']
sensors_cfg_arr = conf['sensors']
roomName = conf['roomName']
def main_loop():
    sensor_read_freq_secs = conf.get('sensor_read_freq_secs', 30)
    while True:
        global i
        i+=1
        now = datetime.datetime.now(targetTz)

        for a in sensors_cfg_arr:
            reading = ()
            publishableDoc = None
            readingType = a.get('type') 
            if(readingType == 'ow'):
                info('reading ow sensor')
                reading = ow.read(a.get('addr'))
                publishableDoc = readingObj(now, reading)
            elif(readingType == 'dht'):
                info('reading dht sensor')
                reading = dht.read(a.get('addr'))
                publishableDoc = readingObj(now, reading)
            elif(readingType == 'air_quality_serial'):
                if(not aqss.inited()):
                    serialDevice = a.get('serialDevice')
                    aqss.init(serialDevice)
                info('reading air quality sensor [serial]')
                reading = aqss.read(output_fmt, targetTz)
                if(reading):
                    publishableDoc = airquality_readingObj(reading)
                else:
                    publishableDoc = None
            elif(readingType == 'serial_float'):
                if(not ssf.inited()):
                    serialDevice = a.get('serialDevice')
                    ssf.init(serialDevice)
                info('reading sensor [serial] float')
                reading = ssf.read()
                info(reading)
                publishableDoc = {'current':reading}
                info(publishableDoc)
            else:
                info('unsupported reading type ', readingType)
                continue
            if(not publishableDoc):
                warning('skipping malformed reading')
                continue
            topic = a.get('topic','')
            if(topic):
                info('publishing ', publishableDoc, ' to mqtt ', topic)
                client.publish(topic, json.dumps(publishableDoc))    
            if(a.get('influx')):
                influks.write('readings',publishableDoc)

        if(i%10==0 and conf['gdocs']):
            info("GDOCS object:", conf['gdocs'])
            gs.append_reading(reading)
        time.sleep(sensor_read_freq_secs)

def readingObj(now, reading):
    if(not reading or len(reading)<1):
        warning('Invalid reading data. Expected at least temp')
        return None
    obj = {'temp':reading[0],'tstamp':now.strftime(output_fmt), 'roomName':roomName}
    if len(reading)>1:
        obj['hum'] = reading[1]
    return obj

def airquality_readingObj(reading):
    if(len(reading)!=2):
        warning('invalid data format read from air quality sensor file')
        return
    jason = {'level':reading[1],'tstamp':reading[0], 'roomName':roomName}
    info('airquality_readingObj\n', json.dumps(jason))
    return jason

def main(argv=None):
    #info('Logging sensor measurements to {0} every {1} seconds.'.format(conf['gdocs']['doc_name'], conf['sensor_read_freq']))
    if argv is None:
        argv = sys.argv
    try:
        opts, args = getopt.getopt(argv[1:], "h", ["help"])
    except getopt.error, msg:
        print(msg)
        sys.exit(2)
    main_loop()

if __name__ == "__main__":
    main()
