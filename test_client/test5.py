from datetime import datetime, timedelta

now = datetime.now()
start = now - timedelta(seconds=3600)
# endtime = str(now.date()) + 'T' + str(now)[11:19] + 'Z'
# starttime = str(start.date()) + 'T' + str(start)[11:19] + 'Z'
# print(starttime, endtime)

# if now.month in (11, 12, 1, 2):
#   season = 'WINTER'
# elif now.month in (6, 7, 8):
#   season = 'SUMMER'
# else:
#   season = 'OTHER'

# print(season)
# print(now.date)
# print(now.day)
# 2023-09-15 07:17:21.960643+00:00
# 2023-09-15 16:18:53.142767

print(now)
print(start)

gap = now - start
print(gap.seconds)