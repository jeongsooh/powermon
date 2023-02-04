#-*- coding: utf-8 -*-


# from rest_framework.response import Response
# from rest_framework.views import APIView
# import json
from datetime import datetime, timedelta
import time


# data = []
# start_time = time.time()
# current_time = time.gmtime()
# current_minutes = current_time.tm_min


# print(start_time)
# print(current_time)
# print(current_minutes)

# msg = [2, '1674614469253', 'MeterValues', {1,2}]

# if msg[3]:
#   print (msg)
# else:
#   print('msg is None')

# timeband = [0, 0, 0, 0]
# line_data = [str(data_time), meterValue['sensor_id'],data['probe'],data['power'][count],data['powerfactor'][count],data['voltage'][count]]
# line_data = ['2023-01-21 03:51:59.59', 'gre000200' , 0, 95214, 88, 232105]
# timeobj = datetime.strptime(line_data[0], '%Y-%m-%d %H:%M:%S.%f')
timeobj = datetime.utcnow()
print(timeobj.date(), timeobj.hour, timeobj.minute)
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

start_timeobj = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=9)
print(start_timeobj.date(), start_timeobj.hour, start_timeobj.minute)
print(type(start_timeobj.date()), type(start_timeobj.hour), type(start_timeobj.minute))
print(type(str(start_timeobj.date())), type(str(start_timeobj.hour)), type(start_timeobj.minute))
# now = datetime.now()
# print(now)
# next_alarm = now + timedelta(minutes=15 - now.minute % 15)
# delta = next_alarm - now
# print(delta)


# while True:
#     now = datetime.now()
#     next_alarm = now + timedelta(minutes=2 - now.minute % 2)
#     delta = next_alarm - now
#     print('Alarm:', next_alarm.strftime("%H:%M:%S"))
#     time.sleep(delta.total_seconds())