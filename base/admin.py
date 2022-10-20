from django.contrib import admin
from .models import Item

# Register your models here.

class ItemAdmin(admin.ModelAdmin):
  list_display = ('msg_name', 'sensor_id','transaction_id', 'timestamp', 'data', 'created',)

admin.site.register(Item, ItemAdmin)