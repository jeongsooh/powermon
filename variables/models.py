from django.db import models
from user.models import User
from sensor.models import Sensor

# Create your models here.

class Variables(models.Model):
  user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='관리자아이디')
  sensorid = models.ForeignKey(Sensor, on_delete=models.CASCADE, verbose_name='센서아이디')
  peak_target = models.IntegerField(verbose_name='피크목표')
  baselined = models.IntegerField(verbose_name='요금적용전력')
  contracted = models.IntegerField(verbose_name='기본계약전력')
  register_dttm = models.DateTimeField(auto_now_add=True, verbose_name='등록일시')

  def __str__(self):
    return str(self.sensorid)

  class Meta:
    db_table = 'powermon_variables'
    verbose_name = '운용변수'
    verbose_name_plural = '운용변수'

