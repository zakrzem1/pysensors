from pyhocon import ConfigFactory
configuration = ConfigFactory.parse_file('pysensors.conf')

conf = {}
conf['sensor_read_freq_secs'] = configuration.get_int('sensor_read_freq_secs',30)
conf['roomName'] = configuration.get_string('roomName','Nick')
conf['gdocs'] = None
gdocs_email = configuration.get_string('gdocs.email','')
gdocs_doc_name = configuration.get_string('gdocs.doc_name','')
gdocs_key_file = configuration.get_string('gdocs.key_file','')
if(gdocs_email and gdocs_doc_name and gdocs_key_file):
    conf['gdocs'] = {}
    conf['gdocs']['email'] = gdocs_email
    conf['gdocs']['doc_name'] = gdocs_doc_name
    conf['gdocs']['key_file'] = gdocs_key_file

conf['mqtt'] = {
    "topic_resolution": configuration.get_string('mqtt.topic_resolution', 'home/sensors/temperature/kitchen/resolution'),
    "broker_host": configuration.get_string('mqtt.broker_host','localhost')
}

conf['sensors'] = configuration.get('sensors')

conf['influx'] = {
    "host": configuration.get_string('influx.host', '127.0.0.1'),
    "dbname": configuration.get_string('influx.dbname', 'readings'),
    "username": configuration.get_string('influx.username', None),
    "password": configuration.get_string('influx.password', None)
}