from sensor.models import Sensor
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

import json, pandas as pd

from energyinfo.models import Energyinfo
from clients.models import Clients
from sensor.kepco_tariff import calculate_price_perload
from energyinfo.tasks import get_energy_info

def getStats(period, sensors):
  # Calulate time range for statistics
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
    s1 = str(current)[:8] + '01 00:00:00'
    e1 = str(current)[:19]
    start = datetime.strptime(s1, '%Y-%m-%d %H:%M:%S')
    end = datetime.strptime(e1, '%Y-%m-%d %H:%M:%S')
  elif period == 'tt_stats':
    current = datetime.now()
    s1 = '2023-01-01 00:00:00'
    e1 = str(current)[:19]
    start = datetime.strptime(s1, '%Y-%m-%d %H:%M:%S')
    end = datetime.strptime(e1, '%Y-%m-%d %H:%M:%S')
  else:
    pass 
  # print(start, end, sensors)
  # energy statisctics
  en_stats = {'en_all':0, 'en_h':0, 'en_m':0, 'en_l':0}
  en_act = {}
  act_list = []

  for sensor in sensors:
    en_act_sensor = {'energy_a':[], 'energy_b':[], 'energy_c':[]}
    energyinfo = Energyinfo.objects.filter(m_date__range=(start, end), sensorid=sensor).values()
    df = pd.DataFrame.from_records(energyinfo)
    if not df.empty:
      en_stats['en_all'] += df['energy_a'].sum() + df['energy_b'].sum() + df['energy_c'].sum()
      df_h = df[((df['m_hour'] >= 13) & (df['m_hour'] < 18)) | (df['m_hour'] == 11)]    # heavy load timeband
      en_stats['en_h'] += df_h['energy_a'].sum() + df_h['energy_b'].sum() + df_h['energy_c'].sum()
      df_m = df[((df['m_hour'] >= 8) & (df['m_hour'] < 11)) | (df['m_hour'] == 12) | ((df['m_hour'] >= 18) & (df['m_hour'] < 22))]    # medium load timeband
      en_stats['en_m'] += df_m['energy_a'].sum() + df_m['energy_b'].sum() + df_m['energy_c'].sum()
      df_l = df[((df['m_hour'] >= 22) | (df['m_hour'] < 8))]    # light load timeband
      en_stats['en_l'] += df_l['energy_a'].sum() + df_l['energy_b'].sum() + df_l['energy_c'].sum()

      en_act_sensor['labels'] = df['m_date'].tolist()
      en_act_sensor['energy_a'] = df['energy_a'].tolist()
      en_act_sensor['energy_b'] = df['energy_b'].tolist()
      en_act_sensor['energy_c'] = df['energy_c'].tolist()
      for count in range(len(en_act_sensor['labels'])) :
        act_list.append(int(df.iloc[count]['energy_a']+df.iloc[count]['energy_b']+df.iloc[count]['energy_c']))
      # print(act_list)
      en_act_sensor['energy_sum'] = act_list
      en_act[sensor] = en_act_sensor

  return en_stats, en_act

def energystatcreate(ownername):
  queryset = Sensor.objects.filter(ownername=ownername).values()
  sensors = [item['sensorid'] for item in queryset]
  lm_stats, lm_act = getStats('lm_stats', sensors)    # last month results
  cm_stats, cm_act = getStats('cm_stats', sensors)    # current month results
  ld_stats, ld_act = getStats('ld_stats', sensors)    # Yesterday results
  cd_stats, cd_act = getStats('cd_stats', sensors)    # today results
  energystat = {
    'lmonth_E': lm_stats['en_all'] / 1000,
    'lmonth_H': lm_stats['en_h'] / 1000,
    'lmonth_M': lm_stats['en_m'] / 1000,
    'lmonth_L': lm_stats['en_l'] / 1000,
    'cmonth_E': cm_stats['en_all'] / 1000,
    'cmonth_H': cm_stats['en_h'] / 1000,
    'cmonth_M': cm_stats['en_m'] / 1000,
    'cmonth_L': cm_stats['en_l'] / 1000,
    'mtrend_E': cm_stats['en_all'] / (lm_stats['en_all'] + 1) * 100,
    'mtrend_H': cm_stats['en_h'] / (lm_stats['en_h'] + 1) * 100,
    'mtrend_M': cm_stats['en_m'] / (lm_stats['en_m'] + 1) * 100,
    'mtrend_L': cm_stats['en_l'] / (lm_stats['en_l'] + 1) * 100,
    'lday_E': ld_stats['en_all'] / 1000,
    'lday_H': ld_stats['en_h'] / 1000,
    'lday_M': ld_stats['en_m'] / 1000,
    'lday_L': ld_stats['en_l'] / 1000,
    'cday_E': cd_stats['en_all'] / 1000,
    'cday_H': cd_stats['en_h'] / 1000,
    'cday_M': cd_stats['en_m'] / 1000,
    'cday_L': cd_stats['en_l'] / 1000,
    'dtrend_E': cd_stats['en_all'] / (ld_stats['en_all'] + 1) * 100,
    'dtrend_H': cd_stats['en_h'] / (ld_stats['en_h'] + 1) * 100,
    'dtrend_M': cd_stats['en_m'] / (ld_stats['en_m'] + 1) * 100,
    'dtrend_L': cd_stats['en_l'] / (ld_stats['en_l'] + 1) * 100,
    'lm_act': lm_act,
    'cm_act': cm_act,
    'ld_act': ld_act,
    'cd_act': cd_act,
  }
  return energystat, sensors

def energymgt_target(userid):
  result_sum = {}
  # deciding time range from where date is restored.
  now = datetime.utcnow()
  start = now - timedelta(seconds=10)
  end_time = str(now.date()) + 'T' + str(now)[11:19] + 'Z'
  start_time = str(start.date()) + 'T' + str(start)[11:19] + 'Z'
  # print(start_time, end_time)

  # sensor list which runs at the moment  
  query_lists = Clients.objects.all()
  # print(query_lists)

  for sensor_id in query_lists:
    results = get_energy_info(str(sensor_id), start_time, end_time)
    print(results, sensor_id)
    result_sum[str(sensor_id)] = results

  print(result_sum)
  power_sum = 1000
  # power_sum = 0
  # for result in result_sum:
  #   power_sum += int(result[0]['power']) + int(result[1]['power']) + int(result[2]['power'])




  mgt_target = {
    'consumed_now': power_sum * 4 / 1000,
    'peakoftoday': 1500 / 1000,
    'peakofmonth': 2000 / 1000,
    'peaktarget': 2500 / 1000,
    'baselined': 3000 / 1000,
    'contracted': 4000 / 1000,
  }

  return mgt_target

def energystatsum(userid):
  queryset = Sensor.objects.filter(ownerid=userid).values()
  sensors = [item['sensorid'] for item in queryset]

  cm_stats, cm_act = getStats('cm_stats', sensors)    # current month results(cm_stats) 
  tt_stats, tt_act = getStats('tt_stats', sensors)    # total energy stats(tt_act)
  # base_fee, total_usage = calculate_price_perload(peakload, highload, lowload, userid) 
  base_fee, total_usage = calculate_price_perload(cm_stats['en_h'] / 1000, cm_stats['en_m'] / 1000, cm_stats['en_l'] / 1000, userid) 
  energystat = {
    'cmonth_E': cm_stats['en_all'] / 1000,
    'cmonth_H': cm_stats['en_h'] / 1000,
    'cmonth_M': cm_stats['en_m'] / 1000,
    'cmonth_L': cm_stats['en_l'] / 1000,
    'tt_act': tt_act,
    'total_amount': total_usage + base_fee
  }
  return energystat, sensors
