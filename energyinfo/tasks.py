# from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS, PointSettings

from celery import shared_task

from clients.models import Clients
from energyinfo.models import Energyinfo
# from django.core.mail import send_mail
# from powermon import settings
# from django.utils import timezone

# get energy info from each sensor
def get_energy_info(sensor_id, start_time, end_time):
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

    # Query script
    query_api = client.query_api()
    m_fields = ["power", "voltage", "powerfactor"]
    m_phase = [0, 1, 2]
    results = []
    for phase_id in m_phase:
        for m_field in m_fields:
            query = 'from(bucket:"powermon")\
            |> range(start:' + str(start_time) + ', stop:' + str(end_time) + ')\
            |> filter(fn:(r) => r._measurement == "power_data")\
            |> filter(fn:(r) => r.sensor_id == "' + sensor_id + '")\
            |> filter(fn:(r) => r.phase_id == "' + str(phase_id) + '")\
            |> filter(fn:(r) => r._field == "' + m_field + '")'
            # |> filter(fn:(r) => r._field == "voltage")'
            result = query_api.query(org=org, query=query)
            print(org)
            print(query)
            print(result)
            # results = []
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

    return results

# deciding time range from where data is restored
def time_range():
  timeobj = datetime.utcnow()
  timestr = str(timeobj)[:10] + 'T' + str(timeobj)[11:13]

  if timeobj.minute < 15 and timeobj.minute >= 0:
      print("band 0 - 15")
      new_timeobj = timeobj - timedelta(hours=1)
      new_timestr = str(new_timeobj)[:10] + 'T' + str(new_timeobj)[11:13]
      m_minute = 'q4'
      start_min = '45:01' 
      end_min = '00:00'
      start_time = new_timestr + ':' + start_min + 'Z'
      end_time = timestr + ':' + end_min + 'Z'
  elif timeobj.minute < 30 and timeobj.minute >= 15:
      print("band 15 - 30")
      m_minute = 'q1'
      start_min = '00:01' 
      end_min = '15:00'
      start_time = timestr + ':' + start_min + 'Z'
      end_time = timestr + ':' + end_min + 'Z'
  elif timeobj.minute < 45 and timeobj.minute >= 30:
      print("band 30 - 45")
      m_minute = 'q2'
      start_min = '15:01' 
      end_min = '30:00'
      start_time = timestr + ':' + start_min + 'Z'
      end_time = timestr + ':' + end_min + 'Z'
  else:
      print("band 45 - 0")
      m_minute = 'q3'
      start_min = '30:01' 
      end_min = '45:00'
      start_time = timestr + ':' + start_min + 'Z'
      end_time = timestr + ':' + end_min + 'Z'

  print(start_time, end_time, timeobj.hour, m_minute)
        
  return start_time, end_time, m_minute 


@shared_task(bind=True)
def send_mail_func(self):
    # deciding time range from where date is restored.
    start_time, end_time, m_minute = time_range()
    s_timeobj = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=9)

    # sensor list which runs at the moment  
    query_lists = Clients.objects.all()
    print(query_lists)

    for sensor_id in query_lists:
        results = get_energy_info(str(sensor_id), start_time, end_time)

        print(results)
        # print('Energy Info from {} for last 15m: Power {:.2f}Wh, Voltage {:.2f}V and pF {:.2f}'.format(sensor_id, results[0][1], results[1][1], results[2][1]))
        if results:
            energy_info = Energyinfo(
                sensorid=str(sensor_id),
                m_date=s_timeobj.date(),
                m_hour=s_timeobj.hour,
                m_minute=str(m_minute),
                energy_a=results[0][1],
                voltage_a=results[1][1],
                pf_a=results[2][1],
                energy_b=results[3][1],
                voltage_b=results[4][1],
                pf_b=results[5][1],
                energy_c=results[6][1],
                voltage_c=results[7][1],
                pf_c=results[8][1],
            )
            energy_info.save()

    return 'Done'

# @shared_task(bind=True)
# def send_mail_func(self):
    # users = get_user_model().objects.all()
    # timezone.localtime(users.date_time)
    # timezone.localtime(users.date_time) + timedelta(days=1)
    # for user in users:
    #     mail_subject = 'Hi! Celery Testing'
    #     message = 'If you like my content, please hit the like button and do subscribe to my channel.'
    #     to_email = user.email
    #     send_mail(
    #         subject = mail_subject, 
    #         message = message, 
    #         from_email = settings.EMAIL_HOST_USER, 
    #         recipient_list = [to_email],
    #         fail_silently=True
    #     )
    # return 'Done'