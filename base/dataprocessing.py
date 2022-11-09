from datetime import datetime, timedelta

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS, PointSettings

import json
import pandas as pd

# You can generate an API token from the "API Tokens Tab" in the UI
token = "hESD55wGdju_OQprnOkWWX1pteBQ9zSZmFrTocCfz4_lKeSniDc1mHfxsq8FdyHSesD0VrsFc0v6Y351BEpUhQ=="
org = "gresystem"
bucket = "powermon"

def ingest_to_database(data):

  meterValue = {
    'msg_name': data['msg_name'],
    'sensor_id': data['sensor_id'],
    'timestamp': data['data'][0]['timestamp'],
    'data': data['data'][0]['sampledValue']
  }

  for data in meterValue['data']:
    if len(data['power']) > len(data['powerfactor']):
      data_len = len(data['power']) 
    else:
      data_len = len(data['powerfactor'])
    for count in range(data_len):
      data_time = datetime.strptime(meterValue['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ') + timedelta(milliseconds=50) * count
      line_data = [str(data_time), meterValue['sensor_id'],data['probe'],data['power'][count],data['powerfactor'][count],data['voltage'][count]]
      print(line_data)

      with InfluxDBClient(url="http://127.0.0.1:8086", token=token, org=org) as client:
        """
        Ingest DataFrame with default tags
        """
        write_api = client.write_api(write_options=SYNCHRONOUS)
        p = Point("power_data") \
          .tag("sensor_id", meterValue['sensor_id']).tag("phase_id", data['probe']) \
          .field("data_time", str(data_time)).field("power", data['power'][count]).field("powerfactor", data['powerfactor'][count]).field("voltage", data['voltage'][count])
        write_api.write(bucket=bucket, record=p)


def power_data_processing(msg, sensor_id):

  if msg[2] == 'BootNotification':
    conf = [3,msg[1],{'status':'Accepted'}]

  elif msg[2] == 'MeterValues':

    data = {
      'msg_name': msg[2],
      'sensor_id': sensor_id,
      'data': msg[3]['meterValue'],
    }

    """
    Ingest DataFrame with default tags
    """
    ingest_to_database(data)

    conf = [3,msg[1],{'status':'Accepted'}]

  elif msg[2] == 'StartTransaction':
    conf = [3,msg[1],{'status':'Accepted','transactionId':2265}]

  elif msg[2] == 'StopTransaction':
    conf = [3,msg[1],{'status':'Accepted','transactionId':2265}]

  else:
    conf = [3,msg[1],{}]

  return conf