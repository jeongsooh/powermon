from django.db import models

# Create your models here.

class Clients(models.Model):
  sensor_id = models.CharField(max_length=64, blank=True, verbose_name='센서아이디')
  channel_name = models.CharField(max_length=64, blank=True, verbose_name='채널이름')
  channel_status = models.CharField(max_length=64, blank=True, verbose_name='채널상태')
  sensor_status = models.CharField(max_length=64, blank=True, verbose_name='센서상태')
  transaction_id = models.CharField(max_length=256, blank=True, verbose_name='트랜젝션아이디')

  def __str__(self):
    return self.sensor_id

  class Meta:
    db_table = 'powermon_clients'
    verbose_name = '센서상태'
    verbose_name_plural = '센서상태'
