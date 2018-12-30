# pysensors #

Few modules constituting an application that reads sensor data (pluggable modules, can be temp/temp+hum/air-quality) and reports either to google spreadsheet or MQTT broker (or both)

Currently air quality sensor integration is through configured file of the format
    
    [ iso8601timestamp ],[air quality int value 0..1023] 

example:
    
    2017-05-19T20:50:21.776442,462.00

### Prerequisites ###

Install required libraries

    sudo pip install paho-mqtt  pyhocon pytz 

For google docs connectivity, install:

    sudo pip install oauth2client gspread

For direct time series upload, install influx db client lib:
    
    sudo pip install influxdb

For DHT/1wire sensors support Install [Adafruit_Python_GPIO](https://github.com/adafruit/Adafruit_Python_GPIO)
and [Adafruit Python DHT Sensor Library](https://github.com/adafruit/Adafruit_Python_DHT#adafruit-python-dht-sensor-library)

### How to run ###

    python pysensors.py

or

    nohup python pysensors.py >/tmp/pysensors.out &

### How do I set up? ###

Create a file `pysensors.conf` with the structure

```
sensor {
	read_freq_secs : 30
}

gdocs {
	email: user@domain.com
	doc_name: sheet name
	key_file: /path/to/google/docs/file.json
}
sensors : [{
        type: dht
        addr: "P8_11"
        topic: location/room/temp
}, {
        type: ow
        addr: "28-00044b2222ff"
        topic: location/room/temp
}, {
        type: "air_quality"
        fromFile: "/tmp/current"
        topic: /location/room/air
}]
mqtt {
    topic_resolution:   some/path/to_alter/resolution
	broker_host:    192.168.1.108
```

MQTT Message format (JSON):

Temperature:
```
{"temp": "24.312", "tstamp": "2017-05-20T23:10:36Z"}
```
Temp+Humidity:
```
{"temp": "24.312", hum:"", tstamp": "2017-05-20T23:10:36Z"}
```
Air quality:
```
{"level": 345, tstamp": "2017-05-20T23:10:36Z"}
```

Mosquitto setup on MAC (temporarily documented here)
====================================================
brew install mosquitto

Config at `/usr/local/etc/mosquitto/mosquitto.conf`
Enable at the start

    brew services start mosquitto

Start ad-hoc:

    mosquitto -c /usr/local/etc/mosquitto/mosquitto.conf

Install time series db

    brew install influxdb

To have launchd start influxdb now and restart at login:
    
    brew services start influxdb

Or, if you don't want/need a background service you can just run:
  
    influxd -config /usr/local/etc/influxdb.conf

To have launchd start grafana now and restart at login:

    brew install grafana

    brew services start grafana

Or, if you don't want/need a background service you can just run:
  grafana-server --config=/usr/local/etc/grafana/grafana.ini --homepath /usr/local/share/grafana cfg:default.paths.logs=/usr/local/var/log/grafana cfg:default.paths.data=/usr/local/var/lib/grafana cfg:default.paths.plugins=/usr/local/var/lib/grafana/plugins

Deployment on raspberry pi
==========================

Python and libraries
--------------------

    sudo apt-get update
    sudo apt-get -y install build-essential python-pip python-dev python-smbus git 
    sudo pip install paho-mqtt pyhocon pytz pyserial influxdb
    
GPIO library
------------

    cd /tmp
    git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
    cd Adafruit_Python_GPIO
    sudo python setup.py install

Temperature sensor library
--------------------------

    cd /tmp
    git clone https://github.com/adafruit/Adafruit_Python_DHT.git
    cd Adafruit_Python_DHT
    sudo python setup.py install

Pysensors module
----------------
Add system user and group

    sudo useradd -r -s /bin/false pysensors
    sudo groupadd pysensors
    sudo adduser pysensors pysensors

    cd /opt
    sudo git clone https://github.com/zakrzem1/pysensors.git    
    sudo chown -R pysensors pysensors
    sudo chgrp -R pysensors pysensors
    sudo chmod -R g+w /opt/pysensors
    

    cd /opt/pysensors;nohup python pysensors.py >/tmp/pysensors.out &
