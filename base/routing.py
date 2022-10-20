from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
  re_path(r'powermon/data/', consumers.PowermonConsumer.as_asgi()),
  # re_path(r'powermon/data/(?P<sensor_id>\w+)/$', consumers.PowermonConsumer.as_asgi()),
]