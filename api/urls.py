from django.urls import path
from . import views

urlpatterns = [
    path('', views.getData),
    path('powermon/data/', views.addItem)
]