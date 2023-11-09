from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import FormView, CreateView, DeleteView, UpdateView

from django.http import HttpResponse, JsonResponse

from django.db.models import Q

from sensor.models import Sensor
from .forms import RegisterForm
from .energystat import energystatcreate, energymgt_target

# Create your views here.

class SensorCreateView(CreateView):
  model = Sensor
  template_name = 'sensor_register.html'
  fields = ['sensorid', 'ownername', 'ownerid', 'category', 'address1', 'address2']
  success_url = '/sensor/list'

class SensorDeleteView(DeleteView):
  model = Sensor
  template_name='sensor_confirm_delete.html'
  success_url = '/sensor/list'

class SensorUpdateView(UpdateView):
  model = Sensor
  template_name='sensor_update.html'
  fields = [ 'sensorid', 'ownername',]
  success_url = '/sensor/list'

class SensorList(ListView):
  model = Sensor
  template_name='sensor.html'
  context_object_name = 'sensorList'
  paginate_by = 2
  queryset = Sensor.objects.all()

  def get_context_data(self, **kwargs):
    context = super(SensorList, self).get_context_data(**kwargs)
    sensor_id = self.request.session['user']
    context['loginuser'] = sensor_id
    return context

class SensorNode(ListView):
  model = Sensor
  template_name='node.html'
  context_object_name = 'sensorList'
  paginate_by = 5
  queryset = Sensor.objects.all().order_by('ownername')

  def get_context_data(self, **kwargs):
    context = super(SensorNode, self).get_context_data(**kwargs)
    user_id = self.request.session['user']
    query = self.request.GET.get("q", None)
    page = self.request.GET.get('page')
    category = self.request.GET.get('category')
    context['loginuser'] = user_id
    context['q'] = query
    context['category'] = category
    context['page']=page
    return context

  def get_queryset(self) :
    queryset = Sensor.objects.all().order_by('ownername')
    query = self.request.GET.get("q", None)
    category = self.request.GET.get('category')
    if query:
      if category=='all':
        queryset = queryset.filter(
          Q(ownername__icontains=query) |
          Q(sensorid__icontains=query) |
          Q(ownerid__icontains=query)
        )
      elif category=='ownername':
        queryset = queryset.filter(           
          Q(ownername__icontains=query))
      elif category=='sensorid':
        queryset = queryset.filter(           
          Q(sensorid__icontains=query))
      elif category=='ownerid':
        queryset = queryset.filter(           
          Q(ownerid__icontains=query))
    return queryset


class SensorDetail(DetailView):
  template_name='sensor_detail.html'
  queryset = Sensor.objects.all()
  context_object_name = 'sensor'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    sensor_id = self.request.session['user']
    context['loginuser'] = sensor_id
    
    return context

class NodeDetail(DetailView):
  template_name='node_detail.html'
  queryset = Sensor.objects.all()
  context_object_name = 'sensor'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    user_id = self.request.session['user']
    queryset = Sensor.objects.filter(sensorid=context['sensor']).values()
    energystat, sensors = energystatcreate(queryset[0]['ownername'])
    mgt_target = energymgt_target(queryset[0]['ownername'])
    # print('in views: ', queryset[0]['ownername'], len(queryset[0]['ownername']))
    context['loginuser'] = user_id
    context['energystat'] = energystat
    context['sensors'] = sensors
    context['mgt_target'] = mgt_target
    
    return context

def fetch_energy_values_ajax(request):
  ownername = request.GET.get('ownername')
  ownername=ownername[:-1]
  print('ownername: ', ownername, len(ownername))
  energystat, sensors = energystatcreate(ownername)
  # print('energystat: ', energystat)

  return JsonResponse(energystat) 
