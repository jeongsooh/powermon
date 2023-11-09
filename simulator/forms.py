from django import forms
# from .models import User

class SensorSimulForm(forms.Form):
  sensorid = forms.CharField(
    error_messages={
      'required': '사용자 아이디를 입력하세요.'
    },
    max_length=64, label='센서 아이디'
  )
  ipaddress = forms.CharField(
    error_messages={
      'required': 'IP 주소를 입력하세요.'
    },
    max_length=64, label='IP 주소'
  )
  portnum = forms.CharField(
    error_messages={
      'required': '포트번호를 다시 입력하세요.'
    },
    max_length=64, label='Port 번호'
  )

  def clean(self):
    cleaned_data = super().clean()
    sensorid = cleaned_data.get('sensorid')
    ipaddress = cleaned_data.get('ipaddress')
    portnum = cleaned_data.get('portnum')
