from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, CreateView, DeleteView, UpdateView
from sensor.models import Sensor
from .forms import RegisterForm

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
  paginate_by = 2
  queryset = Sensor.objects.all().order_by('ownername')

  def get_context_data(self, **kwargs):
    context = super(SensorNode, self).get_context_data(**kwargs)
    sensor_id = self.request.session['user']
    context['loginuser'] = sensor_id
    return context

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
    sensor_id = self.request.session['user']
    context['loginuser'] = sensor_id
    
    return context
