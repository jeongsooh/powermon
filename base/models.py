from django.db import models

# Create your models here.

class Item(models.Model):
  version = models.CharField(max_length=64)
  sensor_id = models.CharField(max_length=64)
  token = models.CharField(max_length=256)
  timestamp = models.DateTimeField(auto_now_add=False)
  data = models.JSONField(default='{}')
  created = models.DateTimeField(auto_now_add=True)
