# from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
import time


# deciding time range from where date is restored.
# start_time, end_time, m_minute = time_range()
start_time = '2023-01-31T00:00:00Z'
end_time = '2023-02-03T23:59:59Z'
sensor_id = 'GRE000202'
utc = 1698895746

dt = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime(utc) )
print(dt, type(dt))
# timeobj = str(datetime.utcfromtimestamp(utc) + timedelta(hours=9)) + 'Z'

# data_time = datetime.strptime(timeobj, '%Y-%m-%d %H:%M:%S.%fZ')

s_timeobj = datetime.strptime(dt, '%Y-%m-%dT%H:%M:%SZ') + timedelta(milliseconds=50)


print(s_timeobj, type(s_timeobj))


