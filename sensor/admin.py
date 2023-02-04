from django.contrib import admin
from .models import Sensor

# Register your models here.

class SensorAdmin(admin.ModelAdmin):
  list_display = ('sensorid', 'ownername', 'ownerid', 'status', 'category', 'address1', 'address2', 'register_dttm')

admin.site.register(Sensor, SensorAdmin)
