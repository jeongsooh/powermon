from datetime import datetime, timedelta

# from influxdb_client import InfluxDBClient, Point, WritePrecision
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS, PointSettings

# You can generate an API token from the "API Tokens Tab" in the UI
token = "hESD55wGdju_OQprnOkWWX1pteBQ9zSZmFrTocCfz4_lKeSniDc1mHfxsq8FdyHSesD0VrsFc0v6Y351BEpUhQ=="
org = "gresystem"
bucket = "powermon"

# Store the URL of your InfluxDB instance
url="http://localhost:8086"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

# deciding time range from where data is restored
def time_range():
  timeobj = datetime.utcnow()

  if timeobj.minute < 15 and timeobj.minute >= 0:
      print("band 0 - 15")
      new_timeobj = timeobj - timedelta(hours=1)
      m_minute = 'q4'
      start_min = '45:01' 
      end_min = '00:00'
      start_time = str(new_timeobj.date()) +'T'+ str(new_timeobj.hour) + ':' + start_min + 'Z'
      end_time = str(timeobj.date()) +'T'+ str(timeobj.hour) + ':' + end_min + 'Z'
  elif timeobj.minute < 30 and timeobj.minute >= 15:
      print("band 15 - 30")
      m_minute = 'q1'
      start_min = '00:01' 
      end_min = '15:00'
      start_time = str(timeobj.date()) +'T'+ str(timeobj.hour) + ':' + start_min + 'Z'
      end_time = str(timeobj.date()) +'T'+ str(timeobj.hour) + ':' + end_min + 'Z'
  elif timeobj.minute < 45 and timeobj.minute >= 30:
      print("band 30 - 45")
      m_minute = 'q2'
      start_min = '15:01' 
      end_min = '30:00'
      start_time = str(timeobj.date()) +'T'+ str(timeobj.hour) + ':' + start_min + 'Z'
      end_time = str(timeobj.date()) +'T'+ str(timeobj.hour) + ':' + end_min + 'Z'
  else:
      print("band 45 - 0")
      m_minute = 'q3'
      start_min = '30:01' 
      end_min = '45:00'
      start_time = str(timeobj.date()) +'T'+ str(timeobj.hour) + ':' + start_min + 'Z'
      end_time = str(timeobj.date()) +'T'+ str(timeobj.hour) + ':' + end_min + 'Z'

  print(start_time, end_time, m_minute)
        
  return start_time, end_time, m_minute 

# start_time = "2023-02-03 0:15:01"
# s_timeobj = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
# Query script
# p = {
#   "start": s_timeobj,
#   "stop": s_timeobj + timedelta(minutes=15)
# }

# start_time = 2023-02-03T17:15:01Z
# stop_time = 2023-02-03T17:30:00Z

start_time, end_time, m_minute = time_range()

query_api = client.query_api()
m_fields = ["power", "voltage", "powerfactor"] 
m_phase = [0, 1, 2]
results = []

for phase_id in m_phase:
  for m_field in m_fields:
    query = 'from(bucket:"powermon")\
    |> range(start:' + str(start_time) + ', stop:' + str(end_time) + ')\
    |> filter(fn:(r) => r._measurement == "power_data")\
    |> filter(fn:(r) => r.sensor_id == "GRE000202")\
    |> filter(fn:(r) => r.phase_id == "' + str(phase_id) + '")\
    |> filter(fn:(r) => r._field == "' + m_field + '")'
    result = query_api.query(org=org, query=query)
    for table in result:
      field_value = 0
      for record in table.records:
        field_value += record.get_value()
      if m_field == 'power':
        results.append((record.get_field(), field_value / len(table.records) / 1000 / 4))  # 15분 평균을 Wh로 환산하기 위해서 4로 나눠줌
      elif m_field == 'voltage':
        results.append((record.get_field(), field_value / len(table.records) / 1000))
      else:
        results.append((record.get_field(), field_value / len(table.records)))
      field_value = 0

print(results)
print('Energy Info for last 15m: Power {:.2f}Wh, Voltage {:.2f}V and pF {:.2f}'.format(results[0][1], results[1][1], results[2][1]))
