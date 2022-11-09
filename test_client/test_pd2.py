from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS, PointSettings

import random
import json
import pandas as pd

# You can generate an API token from the "API Tokens Tab" in the UI
token = "hESD55wGdju_OQprnOkWWX1pteBQ9zSZmFrTocCfz4_lKeSniDc1mHfxsq8FdyHSesD0VrsFc0v6Y351BEpUhQ=="
org = "gresystem"
bucket = "powermon2"

data = {
  'msg_name': 'data',
  'sensor_id': 'gresystem000001',
  'transaction_id': '123456789',
  'timestamp': str(datetime.now()),
  'data': [
    {
      'probe_id': 1,
      'probe_type': 'CT',
      'power': random.sample(range(1000, 3000), 20),
      'pf': random.sample(range(60, 100), 20),
      'voltage': random.randint(212, 228)
      # 'power': [20, 30, 20, 30, 40, 50, 30, 30, 20, 20],
      # 'pf': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
      # 'voltage': 220
    },
    {
      'probe_id': 2,
      'probe_type': 'CT',
      'power': random.sample(range(1000, 3000), 20),
      'pf': random.sample(range(60, 100), 20),
      'voltage': random.randint(212, 228)
    },
    {
      'probe_id': 3,
      'probe_type': 'CT',
      'power': random.sample(range(1000, 3000), 20),
      'pf': random.sample(range(60, 100), 20),
      'voltage': random.randint(212, 228)
    }
  ]
} 

print(data)

# for probe in range(0, 3):
#   df = pd.DataFrame(data=data['data'][probe], columns=['sensor_id', 'timestamp', 'probe_id', 'power', 'pf', 'voltage'])
#   df['sensor_id'] = data['sensor_id']
#   for i in range(0, 20):
#     df['timestamp'].iloc[i] = pd.to_datetime(data['timestamp']) + pd.Timedelta(milliseconds=50) * i

#   print(df)

#   with InfluxDBClient(url="http://127.0.0.1:8086", token=token, org=org) as client:

#     """
#     Ingest DataFrame with default tags
#     """
#     point_settings = PointSettings(**{"type": "50miliseconds"})
#     point_settings.add_default_tag("example-name", "ingest-data-frame")

#     write_api = client.write_api(write_options=SYNCHRONOUS, point_settings=point_settings)
#     write_api.write(bucket=bucket, record=df, data_frame_measurement_name="power-monitor-df")



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