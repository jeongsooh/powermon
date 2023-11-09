from django.db import models

# Create your models here.

class Item(models.Model):
  msg_name = models.CharField(max_length=64, verbose_name='메세지이름')
  sensor_id = models.CharField(max_length=64, verbose_name='센서아이디')
  transaction_id = models.CharField(max_length=256, verbose_name='트랜젝션아이디')
  timestamp = models.DateTimeField(auto_now_add=False, null=True, verbose_name='생성일시')
  data = models.TextField(verbose_name='메세지본문')
  msg_direction = models.IntegerField(verbose_name='메세지디렉션')
  created = models.DateTimeField(auto_now_add=True, verbose_name='등록일시')

  def __str__(self):
    return self.sensor_id

  class Meta:
    db_table = 'powermon_item'
    verbose_name = '메세지정보'
    verbose_name_plural = '메세지정보'