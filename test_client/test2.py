from datetime import datetime, timedelta

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


count = 24001
max_count = 100

if (count // max_count) % 2 == 1:
  print("홀수")
else:
  print("짝수")