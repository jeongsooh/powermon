# from datetime import datetime, timedelta

from datetime import datetime, timedelta
import time
import random
import json
import pandas as pd


# org_data = [2, '1009261615', 'MeterValues', 
#   {
#     'connectorId': 1, 
#     'transactionId': 2265, 
#     'meterValue': [
#       {
#         'timestamp': '2022-11-03T15:14:20.506Z', 
#         'sampledValue': [
#           {
#             'probe': 0, 
#             'probeType': 'CT', 
#             'power': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
#             'powerfactor': [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100], 
#             'voltage': [6249, 6251, 6252, 6252, 6250, 6248, 6241, 6236, 6226, 6216, 6207, 6205, 6207, 6211, 6215, 6219, 6219, 6217, 6216]
#           }, 
#           {
#             'probe': 1, 
#             'probeType': 'CT', 
#             'power': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
#             'powerfactor': [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 0, 100, 100, 100, 100, 100, 100], 
#             'voltage': [6209, 6207, 6206, 6206, 6203, 6200, 6195, 6192, 6184, 6176, 6167, 6162, 6163, 6168, 6172, 6175, 6176, 6179, 6183]
#           }, 
#           {
#             'probe': 2, 
#             'probeType': 'CT', 
#             'power': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
#             'powerfactor': [0, -100, 0, 0, 50, 0, 0, -100, 0, 0, -100, 0, 0, 50, 0, 0, 0, -100, 0], 
#             'voltage': [229594, 229604, 229614, 229620, 229623, 229624, 229626, 229626, 229618, 229601, 229581, 229556, 229530, 229506, 229483, 229466, 229462, 229471, 229484]
#           }
#         ]
#       }
#     ]
#   }
# ]

# data2 = {
#   'msg_name': org_data[2],
#   'sensor_id': 'gre0001',
#   'data': org_data[3]['meterValue'],
# }

# print(data2)

# meterValue = {
#   'msg_name': data2['msg_name'],
#   'sensor_id': data2['sensor_id'],
#   'timestamp': data2['data'][0]['timestamp'],
#   'data': data2['data'][0]['sampledValue']
# }

# print(meterValue)

# for data in meterValue['data']:
#   if len(data['power']) > len(data['powerfactor']):
#     data_len = len(data['power']) 
#   else:
#     data_len = len(data['powerfactor'])
#   for count in range(data_len):
#     data_time = datetime.strptime(meterValue['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ') + timedelta(milliseconds=50) * count
#     line_data = [str(data_time), meterValue['sensor_id'],data['probe'],data['power'][count],data['powerfactor'][count],data['voltage'][count]]
#     print(line_data)


# count = 24001
# max_count = 100

# if (count // max_count) % 2 == 1:
#   print("홀수")
# else:
#   print("짝수")


# '2022-11-03T15:14:20.506Z'

# now = datetime.now()

# print(datetime.datetime.now())
# print(datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'))

# time1 = str(datetime.datetime.now())
# time2 = str(datetime.datetime.now() + datetime.timedelta(milliseconds=100))
# print('time1: {} time2: {}'.format(time1, time2))

# 2022-11-16 14:47:59.264501 gre000001 1 2527 76 216
# 2022-11-16 14:47:59.314501 gre000001 1 2985 71 224
# 2022-11-16 14:47:59.364501 gre000001 1 2643 63 217
# 2022-11-16 14:47:59.414501 gre000001 1 2597 92 211



time1 = '2023-01-21 02:32:07.22'
time2 = '2023-01-21 02:32:07.27'

timeobj1 = datetime.strptime(time1, '%Y-%m-%d %H:%M:%S.%f')
timeobj2 = datetime.strptime(time2, '%Y-%m-%d %H:%M:%S.%f')
timeobj3 = timeobj1 + timedelta(seconds=1)
power = 0
while timeobj1 < timeobj3:
  power += 1
  timeobj1 = timeobj2 + timedelta(seconds=1)

print('=============power===========', power)
print('=============timeobj1===========', timeobj1)

timeobj4 = datetime.strptime(time1[:19], '%Y-%m-%d %H:%M:%S')
print('timeobj2 = ', str(timeobj2)[:19])


if time1 < time2:
  print('time1 is "Proceeding": ', timeobj1.second, timeobj2.second)
elif time1 > time2:
  print('time1 is "Following": ', timeobj1.minute, timeobj2.minute)
else:
  print('both are same time": ', timeobj1.minute, timeobj2.minute)

# print(timeobj1.date())
# data[1] = 'gre000000'

class EnergyInfo():
  sensorid = None,
  date = '1970-01-01',
  time_band = '',     # band15, band 30, band45, band 60
  data = [
    {'energy':0, 'pf':0, 'voltage':0}, {'energy':0, 'pf':0, 'voltage':0}, {'energy':0, 'pf':0, 'voltage':0}
  ]

temp_energyInfo = EnergyInfo()
active_sensor = {'gre000000': temp_energyInfo,}

# if not data[1] in active_sensor:
if not 'gre000000' in active_sensor:
  print('new sensor attached')
  energyInfo = EnergyInfo()
  active_sensor[data[1]] = energyInfo
else:
  energyInfo = active_sensor['gre000000']

print(energyInfo.date)
print(energyInfo.data[0]['voltage'])