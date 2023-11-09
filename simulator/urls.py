from django.urls import path
from . import views

urlpatterns = [
    path('', views.simulator),
    # path('start/', views.start),
    # path('stop/', views.stop),
]