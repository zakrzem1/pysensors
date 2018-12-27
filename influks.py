from influxdb import InfluxDBClient
from config import conf
import pytz
import datetime

client = InfluxDBClient(host=conf['influx']['host'], port=8086, database=conf['influx']['dbname'], username=conf['influx']['username'], password=conf['influx']['password'])
targetTz = pytz.timezone('UTC')
output_fmt = '%Y-%m-%dT%H:%M:%SZ'
previous_point = {}

def write(measurement, fields={}, tags={}, outputFormat='%Y-%m-%dT%H:%M:%SZ'):
    global previous_point
    now = datetime.datetime.now(targetTz)
    current_point = {
        "measurement": measurement,
        "tags": tags,
        "time": now.strftime(outputFormat),
        "fields": fields
    } 
    if(zero(previous_point) and not zero(current_point)):
        client.write_points([previous_point, current_point])
    elif(not zero(previous_point)):
        client.write_points([current_point])
    previous_point = current_point


def zero(some_point):
    return not any(some_point.get('fields',{}).values())
