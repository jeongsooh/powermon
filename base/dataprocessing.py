from datetime import datetime, timedelta

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS, PointSettings

import time
import json
import random
import pandas as pd 
from queue import Queue

from clients.models import Clients

sensor_data_queue = Queue()

# You can generate an API token from the "API Tokens Tab" in the UI
token = "hESD55wGdju_OQprnOkWWX1pteBQ9zSZmFrTocCfz4_lKeSniDc1mHfxsq8FdyHSesD0VrsFc0v6Y351BEpUhQ=="
org = "gresystem"
bucket = "powermon"

energy_data = {'sensor_id': '', 'date': '', 'time_band': '', 'probe_id': 0, 'energy': 0, 'pf': 0, 'voltage': 0}

def ingest_to_energydb(data):

  sensor_data_queue.put(data)

def ingest_to_database(r_data):

  for num in range(len(r_data['m_data'])):

    meterValue = {
      'msg_name': r_data['msg_name'],
      'sensor_id': r_data['sensor_id'],
      'timestamp': r_data['m_data'][num]['timestamp'],
      'data': r_data['m_data'][num]['sampledValue']
    }

    for data in meterValue['data']:
      if len(data['power']) > len(data['powerfactor']):
        data_len = len(data['power'])
      else:
        data_len = len(data['powerfactor'])

      duration = 1000 / data_len

      meter_time = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime(int(meterValue['timestamp'])))

      for count in range(data_len):
        data_time = datetime.strptime(meter_time, '%Y-%m-%dT%H:%M:%SZ') + timedelta(milliseconds=duration) * count
        # line_data = [str(data_time), meterValue['sensor_id'],data['probe'],data['power'][count],data['powerfactor'][count],data['voltage'][count]]
        # print(line_data)
        # ingest_to_energydb(line_data)   # ingest to energy databases for billing and payment

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

    if msg[3]:
      data = {
        'msg_name': msg[2],
        'sensor_id': sensor_id,
        'm_data': msg[3]['meterValue']
      }

      """
      Ingest DataFrame with default tags
      """
      ingest_to_database(data)

    conf = [3,msg[1],{'status':'MVAccepted'}]

  elif msg[2] == 'StartTransaction':
    transaction_id = random.randint(1000001, 9999999)
    Clients.objects.filter(sensor_id=sensor_id).update(transaction_id=transaction_id)
    conf = [3,msg[1],{'status':'Accepted','transactionId':transaction_id}]

  elif msg[2] == 'StopTransaction':
    transaction_id = msg[3]['transactionId']
    conf = [3,msg[1],{'status':'Accepted','transactionId':transaction_id}]

  elif msg[2] == 'StatusNotification':
    conf = [3,msg[1],{}]

  else:
    conf = [3,msg[1],{'status':'Message unknown'}]

  return conf