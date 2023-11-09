from django.shortcuts import render, redirect
import uuid

from .forms import SensorSimulForm

# Create your views here.

def simulator(request):
  if request.method == 'POST':
    form = SensorSimulForm(request.POST)
    if form.is_valid():
      ocpp_req = {
        "msg_direction" : 2,
        "connection_id" : str(uuid.uuid4()),
        "sensorid": form.data.get('sensorid'),
        "ipaddress": form.data.get('ipaddress'),
        'portnum': form.data.get('portnum'),
      }
      # ocpp_conf = ocpp_request(ocpp_req)
      ocpp_conf = ocpp_req

      return render(request, 'simulator.html', {'form': form, 'conf': ocpp_conf})
  else:
    form = SensorSimulForm()
  return render(request, 'simulator.html', {'form': form})

