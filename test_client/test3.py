#-*- coding: utf-8 -*-


# from rest_framework.response import Response
# from rest_framework.views import APIView
import json, pandas as pd
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import time

period = 'cm_stats'
sensorid = 'GRE00205'
act = {}
act_sub = {}
act_list = []

if period == 'ld_stats':
    start = datetime.combine(date.today(),datetime.min.time()) -timedelta(days=1)
    end = start+timedelta(days=1)-timedelta(seconds=1)
elif period == 'cd_stats':
    start = datetime.combine(date.today(),datetime.min.time())
    current = datetime.now()
    end = datetime.strptime(str(current)[:19], '%Y-%m-%d %H:%M:%S')
elif period == 'lm_stats':
    current = datetime.now()
    delta = relativedelta(months=1)
    s1 = str(current - delta)[:8] + '01 00:00:00'
    e1 = str(current)[:8] + '01 00:00:00'
    start = datetime.strptime(s1, '%Y-%m-%d %H:%M:%S')
    end = datetime.strptime(e1, '%Y-%m-%d %H:%M:%S') - timedelta(seconds=1)
elif period == 'cm_stats':
    current = datetime.now()
    delta = relativedelta(months=1)
    s1 = str(current)[:8] + '01 00:00:00'
    e1 = str(current)[:19]
    start = datetime.strptime(s1, '%Y-%m-%d %H:%M:%S')
    end = datetime.strptime(e1, '%Y-%m-%d %H:%M:%S')
else:
    pass 

print(start.day, end)

df = pd.read_csv('./sample.csv')
print(df)
en_all = df['energy_a'].sum() + df['energy_b'].sum() + df['energy_c'].sum()
# print(en_all)
df_h = df[((df['m_hour'] >= 13) & (df['m_hour'] < 18)) | (df['m_hour'] == 11)]    # heavy load timeband
en_h = df_h['energy_a'].sum() + df_h['energy_b'].sum() + df_h['energy_c'].sum()
# print(en_h)
df_m = df[((df['m_hour'] >= 8) & (df['m_hour'] < 11)) | (df['m_hour'] == 12) | ((df['m_hour'] >= 18) & (df['m_hour'] < 22))]    # medium load timeband
en_m = df_m['energy_a'].sum() + df_m['energy_b'].sum() + df_m['energy_c'].sum()
# print(en_m)
df_l = df[((df['m_hour'] >= 22) | (df['m_hour'] < 8))]    # light load timeband
en_l = df_l['energy_a'].sum() + df_l['energy_b'].sum() + df_l['energy_c'].sum()
# print(en_l)
# print(en_h + en_m + en_l)

labels = [item for item in df['m_date']]
energy = [item for item in df['energy_a']]
energy_a = [item for item in df['energy_a']]
energy_b = [item for item in df['energy_b']]
energy_c = [item for item in df['energy_c']]

for count in range(len(df['m_date'])) :
    act_list.append(df.iloc[count]['energy_a']+df.iloc[count]['energy_b']+df.iloc[count]['energy_c'])
# print(labels)
print(energy_a)
print(energy_b)
print(energy_c)
print(act_list)


e_stat = {'sensorid': sensorid, 'labels': labels, 'data': energy}
# print(labels)
# print(energy)

username = 'jeongsooh1'
print(len(username))
# data = []
# start_time = time.time()
# current_time = time.gmtime()
# current_minutes = current_time.tm_min


# print(start_time)
# print(current_time)
# print(current_minutes)

# msg = [2, '1674614469253', 'MeterValues', {1,2}]


#######################################
### Influxdb time                   ###
#######################################
# timeband = [0, 0, 0, 0]
# line_data = [str(data_time), meterValue['sensor_id'],data['probe'],data['power'][count],data['powerfactor'][count],data['voltage'][count]]
# line_data = ['2023-01-21 03:51:59.59', 'gre000200' , 0, 95214, 88, 232105]
# timeobj = datetime.strptime(line_data[0], '%Y-%m-%d %H:%M:%S.%f')
# timeobj = datetime.utcnow()
# timestr = str(timeobj)[:10] + 'T' + str(timeobj)[11:13]
# print(timestr)
# print(timeobj.date(), timeobj.hour, timeobj.minute)
# if timeobj.minute < 15 and timeobj.minute >= 0:
#     print("band 0 - 15")
#     new_timeobj = timeobj - timedelta(hours=1)
#     new_timestr = str(new_timeobj)[:10] + 'T' + str(new_timeobj)[11:13]
#     m_minute = 'q4'
#     start_min = '45:01' 
#     end_min = '00:00'
#     start_time = new_timestr + ':' + start_min + 'Z'
#     end_time = timestr + ':' + end_min + 'Z'
# elif timeobj.minute < 30 and timeobj.minute >= 15:
#     print("band 15 - 30")
#     m_minute = 'q1'
#     start_min = '00:01' 
#     end_min = '15:00'
#     start_time = timestr + ':' + start_min + 'Z'
#     end_time = timestr + ':' + end_min + 'Z'
# elif timeobj.minute < 45 and timeobj.minute >= 30:
#     print("band 30 - 45")
#     m_minute = 'q2'
#     start_min = '15:01' 
#     end_min = '30:00'
#     start_time = timestr + ':' + start_min + 'Z'
#     end_time = timestr + ':' + end_min + 'Z'
# else:
#     print("band 45 - 0")
#     m_minute = 'q3'
#     start_min = '30:01' 
#     end_min = '45:00'
#     start_time = timestr + ':' + start_min + 'Z'
#     end_time = timestr + ':' + end_min + 'Z'

# print(start_time, end_time, m_minute)

# start_timeobj = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=9)
# print(start_timeobj.date(), start_timeobj.hour, start_timeobj.minute)
# print(type(start_timeobj.date()), type(start_timeobj.hour), type(start_timeobj.minute))
# print(type(str(start_timeobj.date())), type(str(start_timeobj.hour)), type(start_timeobj.minute))

#######################################
###  Alarm generation               ###
#######################################
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