from django import forms
# from django.contrib.auth.hashers import check_password
from .models import Sensor

class RegisterForm(forms.Form):
  sensorid = forms.CharField(
    error_messages={
      'required': '센서아이디를 입력하세요.'
    },
    max_length=64, label='센서아이디'
  )
  ownername = forms.CharField(label='소유주/상호')
  ownerid = forms.CharField(label='관리자아이디')
  status = forms.CharField(label='센서상태')
  category = forms.CharField(label='센서구분')
  address1 = forms.Textarea()
  address2 = forms.TextInput()
  address3 = forms.TextInput()

  def clean(self):
    cleaned_data = super().clean()
    ownerid = cleaned_data.get('ownerid')

    if ownerid is null:
      self.add_error('ownerid', '소유주/상호를 입력해주세요')

# class LoginForm(forms.Form):
#   userid = forms.CharField(
#     error_messages={
#       'required': '사용자 아이디를 입력하세요.'
#     },
#     max_length=64, label='사용자 아이디'
#   )
#   password = forms.CharField(
#     error_messages={
#       'required': '비밀번호를 입력하세요.'
#     },
#     widget=forms.PasswordInput, label='비밀번호'
#   )

#   def clean(self):
#     cleaned_data = super().clean()
#     userid = cleaned_data.get('userid')
#     password = cleaned_data.get('password')

#     if userid and password:
#       try:
#         user = User.objects.get(userid=userid)
#       except User.DoesNotExist:
#         self.add_error('userid', '아이디가 없습니다.')
#         return

#       if password != user.password:
#         self.add_error('password', '비밀번호가 틀렸습니다.')
#       else:
#         self.user_id = user.id