from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, CreateView, DeleteView, UpdateView
from variables.models import Variables
# from .forms import RegisterForm

# Create your views here.

class VariablesCreateView(CreateView):
  model = Variables
  template_name = 'variables_register.html'
  fields = ['user_id', 'sensorid', 'peak_target']
  success_url = '/variables/list'

# class VariablesDeleteView(DeleteView):
#   model = Variables
#   template_name='variables_confirm_delete.html'
#   success_url = '/variables/list'

# class VariablesUpdateView(UpdateView):
#   model = Variables
#   template_name='variables_update.html'
#   fields = [ 'variablesid', 'ownername',]
#   success_url = '/variables/list'

class VariablesList(ListView):
  model = Variables
  template_name='variables.html'
  context_object_name = 'variablesList'
  paginate_by = 5
  queryset = Variables.objects.all()

  def get_context_data(self, **kwargs):
    context = super(VariablesList, self).get_context_data(**kwargs)
    variables_id = self.request.session['user']
    context['loginuser'] = variables_id
    return context

# class VariablesNode(ListView):
#   model = Variables
#   template_name='node.html'
#   context_object_name = 'variablesList'
#   paginate_by = 10
#   queryset = Variables.objects.all().order_by('ownername')

#   def get_context_data(self, **kwargs):
#     context = super(VariablesNode, self).get_context_data(**kwargs)
#     variables_id = self.request.session['user']
#     context['loginuser'] = variables_id
#     return context

# class VariablesDetail(DetailView):
#   template_name='variables_detail.html'
#   queryset = Variables.objects.all()
#   context_object_name = 'variables'

#   def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     variables_id = self.request.session['user']
#     context['loginuser'] = variables_id
    
#     return context

# class NodeDetail(DetailView):
#   template_name='node_detail.html'
#   queryset = Variables.objects.all()
#   context_object_name = 'variables'

#   def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     variables_id = self.request.session['user']
#     context['loginuser'] = variables_id
    
#     return context


