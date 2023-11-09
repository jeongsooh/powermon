from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, CreateView, DeleteView, UpdateView
from django.views.generic.edit import FormView

from .forms import ClientsResetForm
from clients.models import Clients

from base.client_gateway import reset_sensor, remotestart_sensor, remotestop_sensor 
# from .forms import RegisterForm

# Create your views here.

# class ClientsCreateView(CreateView):
#   model = Clients
#   template_name = 'clients_register.html'
#   fields = ['clientsid', 'ownername', 'ownerid', 'category', 'address1', 'address2']
#   success_url = '/clients/list'

# class ClientsDeleteView(DeleteView):
#   model = Clients
#   template_name='clients_confirm_delete.html'
#   success_url = '/clients/list'

# class ClientsUpdateView(UpdateView):
#   model = Clients
#   template_name='clients_update.html'
#   fields = [ 'clientsid', 'ownername',]
#   success_url = '/clients/list'

class ClientsList(ListView):
  model = Clients
  template_name='clients.html'
  context_object_name = 'clientsList'
  paginate_by = 5
  queryset = Clients.objects.all()

  def get_context_data(self, **kwargs):
    context = super(ClientsList, self).get_context_data(**kwargs)
    clients_id = self.request.session['user']
    context['loginuser'] = clients_id
    return context

# class ClientsNode(ListView):
#   model = Clients
#   template_name='node.html'
#   context_object_name = 'clientsList'
#   paginate_by = 10
#   queryset = Clients.objects.all().order_by('ownername')

#   def get_context_data(self, **kwargs):
#     context = super(ClientsNode, self).get_context_data(**kwargs)
#     clients_id = self.request.session['user']
#     context['loginuser'] = clients_id
#     return context

# class ClientsDetail(DetailView):
#   template_name='clients_detail.html'
#   queryset = Clients.objects.all()
#   context_object_name = 'clients'

#   def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     clients_id = self.request.session['user']
#     context['loginuser'] = clients_id
    
#     return context

# class NodeDetail(DetailView):
#   template_name='node_detail.html'
#   queryset = Clients.objects.all()
#   context_object_name = 'clients'

#   def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     clients_id = self.request.session['user']
#     context['loginuser'] = clients_id
    
#     return context


class RemoStartChargeView(FormView):
  template_name = 'clients_reset.html'
  form_class = ClientsResetForm
  success_url = '/clients/list'

  def form_valid(self, form):
    sensor_id = form.data.get('sensor_id')
    remotestart_sensor(sensor_id)

    return super().form_valid(form) 

class RemoStopChargeView(FormView):
  template_name = 'clients_reset.html'
  form_class = ClientsResetForm
  success_url = '/clients/list'

  def form_valid(self, form):
    sensor_id = form.data.get('sensor_id')
    remotestop_sensor(sensor_id)

    return super().form_valid(form) 

class ClientsResetView(FormView):
  template_name = 'clients_reset.html'
  form_class = ClientsResetForm
  success_url = '/clients/list'

  def form_valid(self, form):
    sensor_id = form.data.get('sensor_id')
    reset_sensor(sensor_id)

    return super().form_valid(form) 