from django.db import models

# Create your models here.

class User(models.Model):

  userid = models.CharField(max_length=64, verbose_name='회원아이디')
  password = models.CharField(max_length=128, verbose_name='비밀번호')
  name = models.CharField(max_length=64, verbose_name='회원명/상호')
  email = models.EmailField(max_length=128, verbose_name='이메일')
  phone = models.CharField(max_length=64, verbose_name='전화번호')
  category = models.CharField(max_length=64, verbose_name='회원구분')
  status = models.CharField(max_length=64, verbose_name='회원상태')
  address1 = models.TextField(verbose_name='시/군/구')
  address2 = models.TextField(verbose_name='주소')
  register_dttm = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')

  def __str__(self):
    return self.userid

  class Meta:
    db_table = 'powermon_user'
    verbose_name = '회원'
    verbose_name_plural = '회원'
