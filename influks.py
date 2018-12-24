from influxdb import InfluxDBClient
from config import conf
import pytz
import datetime

client = InfluxDBClient(host=conf['influx']['host'], port=8086, database=conf['influx']['dbname'], username:conf['influx']['username'], password:conf['influx']['password'])
targetTz = pytz.timezone('UTC')
output_fmt = '%Y-%m-%dT%H:%M:%SZ'
previous_point = {}

def write(measurement, fields={}, tags={}):
    now = datetime.datetime.now(targetTz)
    json_body = [
            {
                "measurement": measurement,
                "tags": tags
                "time": now.strftime(outputFormat),
                "fields": fields
            }
        ]
    if(fields):
        client.write_points(json_body)
        previous_point = json_body[0]
