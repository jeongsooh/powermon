from datetime import datetime, timedelta

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS, PointSettings

import random
import json
import pandas as pd

# You can generate an API token from the "API Tokens Tab" in the UI
token = "hESD55wGdju_OQprnOkWWX1pteBQ9zSZmFrTocCfz4_lKeSniDc1mHfxsq8FdyHSesD0VrsFc0v6Y351BEpUhQ=="
org = "gresystem"
bucket = "powermon2"

meterValue = {
  'msg_name': 'data',
  'sensor_id': 'gresystem000001',
  'transaction_id': '123456789',
  'timestamp': str(datetime.now()),
  'data': [
    {
      'probe': 1,
      'probeType': 'CT',
      'power': random.sample(range(1000, 3000), 20),
      'powerfactor': random.sample(range(60, 100), 20),
      'voltage': random.sample(range(209, 231), 20)
    },
    {
      'probe': 2,
      'probeType': 'CT',
      'power': random.sample(range(1000, 3000), 20),
      'powerfactor': random.sample(range(60, 100), 20),
      'voltage': random.sample(range(209, 231), 20)
    },
    {
      'probe': 3,
      'probeType': 'CT',
      'power': random.sample(range(1000, 3000), 20),
      'powerfactor': random.sample(range(60, 100), 20),
      'voltage': random.sample(range(209, 231), 20)
    }
  ]
} 

for data in meterValue['data']:
  if len(data['power']) > len(data['powerfactor']):
    data_len = len(data['power']) 
  else:
    data_len = len(data['powerfactor'])
  for count in range(data_len):
    data_time = datetime.strptime(meterValue['timestamp'], '%Y-%m-%d %H:%M:%S.%f') + timedelta(milliseconds=50) * count
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


# using Table structure
with InfluxDBClient(url="http://127.0.0.1:8086", token=token, org=org) as client:
  query_api = client.query_api()
  tables = query_api.query('from(bucket:"powermon2") |> range(start: -10m)')

  for table in tables:
      # print(table.records)
      for row in table.records:
          print (row.values)
          
  # print("number of tables: ", len(tables))

  


## using csv library
# csv_result = query_api.query_csv('from(bucket:"my-bucket") |> range(start: -10m)')
# val_count = 0
# for row in csv_result:
#     for cell in row:
#         val_count += 1





      # point_settings = PointSettings(**{"type": "50miliseconds"})
      # point_settings.add_default_tag("example-name", "ingest-data-frame")

      # write_api = client.write_api(write_options=SYNCHRONOUS, point_settings=point_settings)
      # write_api.write(bucket=bucket, record=df, 
      #   data_frame_measurement_name="power-monitor-df",
      #   data_frame_tag_columns=['sensor_id', 'probe_id', 'power', 'pf', 'voltage']
      # )



    # write_api = client.write_api(write_options=SYNCHRONOUS)
    # data = json.dumps(message)
    # df = pd.read_json(data)
    # write_api.write(bucket, org, df)

    # """
    # Querying ingested data
    # """
    # query = 'from(bucket:"powermon")' \
    #         ' |> range(start: 0, stop: now())' \
    #         ' |> filter(fn: (r) => r._measurement == "power-monitor-df")' \
    #         ' |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")' \
    #         ' |> limit(n:10, offset: 0)'
    # result = client.query_api().query(query=query)

    # """
    # Processing results
    # """
    # print()
    # print("=== results ===")
    # print()
    # for table in result:
    #     for record in table.records:
    #         print(record)