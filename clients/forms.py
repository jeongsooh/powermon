from django import forms
from clients.models import Clients

class ClientsResetForm(forms.Form):
  sensor_id = forms.CharField(
    error_messages={
      'required': '센서아이디를 입력하세요.'
    },
    max_length=64, label='센서아이디'
  )

  def clean(self):
    cleaned_data = super().clean()
    sensor_id = cleaned_data.get('sensor_id')

    if sensor_id:
      try:
        clients = Clients.objects.get(sensor_id=sensor_id)
      except Clients.DoesNotExist:
        self.add_error('sensor_id', '해당되는 센서가 없습니다.')
        return

      self.sensor_id = clients.id