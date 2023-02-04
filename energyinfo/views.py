from django.shortcuts import render
from django.http import HttpResponse

from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import generics
from rest_framework import mixins
from .models import Energyinfo
# from .serializers import EnergyinfoSerializer

from .tasks import send_mail_func
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json
import zoneinfo

# Create your views here.

class EnergyinfoList(ListView):
  model = Energyinfo
  template_name='energyinfo_list.html'
  context_object_name = 'energyinfoList'
  paginate_by = 2
  queryset = Energyinfo.objects.all()

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    user_id = self.request.session['user']
    context['loginuser'] = user_id
    return context

class EnergyinfoDetail(DetailView):
  template_name='energyinfo_detail.html'
  queryset = Energyinfo.objects.all()
  context_object_name = 'energyinfo'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    user_id = self.request.session['user']
    context['loginuser'] = user_id
    
    return context

class EnergyinfoCreateView(CreateView):
  model = Energyinfo
  template_name = 'energyinfo_register.html'
  fields = ['cpname', 'cpnumber', 'userid', 'energy', 'amount']
  success_url = '/energyinfo'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    user_id = self.request.session['user']
    context['loginuser'] = user_id
    print(context['form'])
    
    return context

class EnergyinfoUpdateView(UpdateView):
  model = Energyinfo
  template_name='energyinfo_update.html'
  fields = ['cpname', 'cpnumber', 'userid', 'energy', 'amount']
  success_url = '/energyinfo'

def dashboard(request):
  username  = request.session.get('user')

  return render(request, 'dashboard.html', {'loginuser': username})

def schedule_mail(request):
    # schedule, created = CrontabSchedule.objects.get_or_create(hour=13, minute=15, timezone=zoneinfo.ZoneInfo('Asia/Seoul'))
    # task = PeriodicTask.objects.create(crontab=schedule, name='schedule_mail_task_'+'4', task='energyinfo.tasks.send_mail_func') #, args=json.dumps([[2,3]]))
    task = PeriodicTask.objects.create(name='schedule_mail_task_'+'4', task='energyinfo.tasks.send_mail_func') #, args=json.dumps([[2,3]]))

    return HttpResponse('Done')


