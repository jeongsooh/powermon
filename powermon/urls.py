from django.contrib import admin
from django.urls import path, include

from user.views import index, logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('user/', include('user.urls')),
    path('sensor/', include('sensor.urls')),
    path('energyinfo/', include('energyinfo.urls')),
    path('clients/', include('clients.urls')),
    path('variables/', include('variables.urls')),
    path('base/', include('base.urls')),
    path('simulator/', include('simulator.urls')),
    path('logout/', logout),
]
