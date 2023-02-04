from django.contrib import admin
from .models import Energyinfo

# Register your models here.

class EnergyinfoAdmin(admin.ModelAdmin):
  list_display = ('sensorid', 'm_date', 'm_hour', 'm_minute', 'energy_a', 'pf_a', 'voltage_a', 'register_dttm')

admin.site.register(Energyinfo, EnergyinfoAdmin)
