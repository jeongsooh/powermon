from django.contrib import admin
from .models import Clients

# Register your models here.

class ClientsAdmin(admin.ModelAdmin):
  list_display = ('sensor_id', 'channel_name', 'channel_status', 'sensor_status', 'transaction_id')

admin.site.register(Clients, ClientsAdmin)
