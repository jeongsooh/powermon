from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'powermon.settings')

app = Celery('powermon')  
app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Seoul')

app.config_from_object(settings, namespace='CELERY')

app.conf.beat_schedule = {
  # 'get_energy_15m': {
  #   'task': 'energyinfo.tasks.get_energy',
  #   'schedule': 900       # 15min * 60sec
  # }
}
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')