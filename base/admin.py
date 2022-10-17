from django.contrib import admin
from .models import Item

# Register your models here.

class ItemAdmin(admin.ModelAdmin):
  list_display = ('version', 'sensor_id','token', 'timestamp', 'data', 'created',)

admin.site.register(Item, ItemAdmin)