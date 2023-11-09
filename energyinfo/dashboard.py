from datetime import datetime, timedelta, date
import random
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from base.dataprocessing import sensor_data_queue

# def show_graph(request,template_name='live_graph.html'):
#     return render(request,template_name)

def fetch_sensor_values_ajax_1(request):
  data={}
  sensor_data = []
  sensor_data_org = sensor_data_queue.get()
  # str(data_time), 'sensor_id', 'probe', 'power', 'powerfactor', 'voltage'
  ok_date=str(sensor_data_org[0][:22])
  sensor_val = sensor_data_org[3]

  sensor_data.append(str(sensor_val)+','+ok_date)
  data['result']=sensor_data
  print(sensor_data)

  return JsonResponse(data) 

def fetch_sensor_values_ajax(request):
  data={}
  sensor_data = []
  data_org = sensor_data_queue.get()
  # str(data_time), 'sensor_id', 'probe', 'power', 'powerfactor', 'voltage'
  ok_date=str(data_org[0])
  ok_date_obj1 = datetime.strptime(ok_date, '%Y-%m-%d %H:%M:%S.%f')
  band_obj = ok_date_obj1 + timedelta(seconds=1)
  sensor_val = data_org[3]
  sensor_tmp = 0
  while ok_date_obj1 < band_obj:
    sensor_tmp += sensor_val

    data_tmp = sensor_data_queue.get()
    date_tmp=str(data_tmp[0])
    ok_date_obj1 = datetime.strptime(date_tmp, '%Y-%m-%d %H:%M:%S.%f')
    sensor_val = data_tmp[3]

  sensor_data_queue.put(data_tmp)
  ok_date = str(band_obj)[:19]
  sensor_data.append(str(sensor_tmp)+','+ok_date)
  data['result']=sensor_data
  print(sensor_data)

  return JsonResponse(data) 

def energyinfoCreate():
    startday = datetime.combine(date.today(),datetime.min.time()) -timedelta(days=1)
    endday = startday+timedelta(days=1)-timedelta(seconds=1)
    if Evmain.objects.filter(systemday__range=(startday,endday)).count() ==0:
        energy = Charginginfo.objects.filter(start_dttm__range=(startday,endday))
        totalenergy=0  
        totalamount=0
        for a in range(energy.count()):
            totalenergy += energy.values()[a]['energy']
            totalamount += energy.values()[a]['amount']
        today = date.today()-timedelta(days=1)
        evmain = Evmain(
            regiCount = Evuser.objects.filter(register_dttm__range=(startday,endday)).count(),
            regiTotal = Evuser.objects.all().count(),
            useCharger = Evcharger.objects.filter(cpstatus='사용중').count(),
            totalCharger = Evcharger.objects.all().count(),
            systemday = today,
            totalenergy = totalenergy,
            totalamount = totalamount
        )
        evmain.save() 
    else :
        Evmain.objects.filter(systemday=date.today()-timedelta(days=1)).update(useCharger = Evcharger.objects.filter(cpstatus='사용중').count())

