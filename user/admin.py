from django.contrib import admin
from .models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
  list_display = ('userid', 'password', 'name', 'email', 'phone', 'category', 'status', 'address1', 'address2', 'register_dttm')

admin.site.register(User, UserAdmin)
