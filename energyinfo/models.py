from django.db import models

# Create your models here.

class Energyinfo(models.Model):
  sensorid = models.CharField(max_length=64, verbose_name='센서아이디')
  m_date = models.DateField(auto_now_add=False, verbose_name='날짜')
  m_hour = models.IntegerField(verbose_name='시간')
  m_minute = models.CharField(max_length=64, verbose_name='분대역구분') # q1, q2, q3, q4
  energy_a = models.IntegerField(verbose_name='A전력량')
  pf_a = models.IntegerField(verbose_name='A파워팩터')
  voltage_a = models.IntegerField(verbose_name='A전압')
  energy_b = models.IntegerField(verbose_name='B전력량')
  pf_b = models.IntegerField(verbose_name='B파워팩터')
  voltage_b = models.IntegerField(verbose_name='B전압')
  energy_c = models.IntegerField(verbose_name='C전력량')
  pf_c = models.IntegerField(verbose_name='C파워팩터')
  voltage_c = models.IntegerField(verbose_name='C전압')
  register_dttm = models.DateTimeField(auto_now_add=True, verbose_name='등록일시')

  # def __str__(self):
  #   return self.chargedname

  class Meta:
    db_table = 'powermon_energyinfo'
    verbose_name = '에너지정보'
    verbose_name_plural = '에너지정보'