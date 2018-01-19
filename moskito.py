import paho.mqtt.client as mqtt
from log import info,warning
from config import conf
mqtt_topic_resolution = conf['mqtt']['topic_resolution']
mqtt_broker_host = conf['mqtt']['broker_host']

def on_connect(client, userdata, rc):
  info("Connected with result code " + str(rc) + " subscribing to " + mqtt_topic_resolution)
  subscribed = client.subscribe(mqtt_topic_resolution)
  info ('subscribed sucess = '+str(mqtt.MQTT_ERR_SUCCESS == subscribed[0])+' msgID: '+str(subscribed[1]))

def on_message(client, userdata, msg):
  info(str(client) + str(userdata))
  info(msg.topic + " on_message " + msg.payload)
  freqToSet = int(str(msg.payload))
  if freqToSet>0 and freqToSet<3600*24:
    info(msg.topic+" setting freq to "+str(freqToSet))
    FREQUENCY_SECONDS = freqToSet
  else:
    warning(msg.topic+" ignoring msg "+msg.payload)

def on_subscribe(mosq, obj, mid, granted_qos):
  info("[on_subscribe] Subscribed: " + str(mid) + " " + str(granted_qos))

def start_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    client.connect(mqtt_broker_host, 1883, 60)
    client.loop_start()
    return client
