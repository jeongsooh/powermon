from django.db import models

# Create your models here.

class Sensor(models.Model):

  sensorid = models.CharField(max_length=64, verbose_name='센서아이디')
  ownername = models.CharField(max_length=64, verbose_name='소유주/상호')
  ownerid = models.CharField(max_length=64, verbose_name='관리자아이디')
  status = models.CharField(max_length=64, verbose_name='센서상태')
  category = models.CharField(max_length=64, verbose_name='센서구분') # main, submain, sub, special
  address1 = models.TextField(verbose_name='시/군/구')
  address2 = models.TextField(verbose_name='상세주소')
  address3 = models.TextField(verbose_name='설치위치')
  register_dttm = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')

  def __str__(self):
    return self.sensorid

  class Meta:
    db_table = 'powermon_sensor'
    verbose_name = '센서'
    verbose_name_plural = '센서'