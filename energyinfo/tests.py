# from django.test import TestCase

# Create your tests here.

from clients.models import Clients

queryset = Clients.objects.all()

print(queryset)
for client in queryset:
  print(client)