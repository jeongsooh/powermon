from django.contrib import admin
from .models import Variables

# Register your models here.

class VariablesAdmin(admin.ModelAdmin):
  list_display = ('user_id', 'sensorid', 'peak_target', 'baselined', 'contracted', 'register_dttm')

admin.site.register(Variables, VariablesAdmin)
