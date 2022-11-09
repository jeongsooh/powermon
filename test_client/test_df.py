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


"""
Write Pandas DataFrame
"""
"""
_now = datetime.utcnow()
_data_frame = pd.DataFrame(data=[["coyote_creek", 1.0], ["coyote_creek", 2.0]],
                            index=[_now, _now + timedelta(hours=1)],
                            columns=["location", "water_level"])

_write_client.write("my-bucket", "my-org", record=_data_frame, data_frame_measurement_name='h2o_feet',
                    data_frame_tag_columns=['location'])
"""


for probe in range(0, 3):
  _now = datetime.utcnow()
  df = pd.DataFrame(data=data['data'][probe], columns=['timestamp', 'sensor_id', 'probe_id', 'power', 'pf', 'voltage'])
  df['sensor_id'] = data['sensor_id']
  for i in range(0, 20):
    df['timestamp'].iloc[i] = pd.to_datetime(data['timestamp']) + pd.Timedelta(milliseconds=50) * i
    # df['_start'].iloc[i] = _now + timedelta(milliseconds=50) * i

  df.set_index('timestamp')
  print(df)

  with InfluxDBClient(url="http://127.0.0.1:8086", token=token, org=org) as client:

    """
    Ingest DataFrame with default tags
    """
    point_settings = PointSettings(**{"type": "50miliseconds"})
    point_settings.add_default_tag("example-name", "ingest-data-frame")

    write_api = client.write_api(write_options=SYNCHRONOUS, point_settings=point_settings)
    write_api.write(bucket=bucket, record=df, 
      data_frame_measurement_name="power-monitor-df",
      data_frame_tag_columns=['sensor_id', 'probe_id', 'power', 'pf', 'voltage']
    )



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