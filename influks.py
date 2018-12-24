from influxdb import InfluxDBClient
from config import conf
import pytz
import datetime

client = InfluxDBClient(host=conf['influx']['host'], port=8086, database=conf['influx']['dbname'], username=conf['influx']['username'], password=conf['influx']['password'])
targetTz = pytz.timezone('UTC')
output_fmt = '%Y-%m-%dT%H:%M:%SZ'
previous_point = {}

def write(measurement, fields={}, tags={}):
    now = datetime.datetime.now(targetTz)
    current_point = {
        "measurement": measurement,
        "tags": tags,
        "time": now.strftime(outputFormat),
        "fields": fields
    }    
    if(not zero(current_point) and zero(previous_point)):
        client.write_points([previous_point, current_point])
    elif(not zero(current_point) and not zero(previous_point)):
        client.write_points([current_point])
    previous_point = current_point


def zero(some_point):
    return not some_point.fields.values().any()