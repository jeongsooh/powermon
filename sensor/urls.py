from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index),
    # path('dashboard/', views.dashboard),
    path('list/', views.SensorList.as_view()),
    path('list/<int:pk>/', views.SensorDetail.as_view()),
    path('update/<int:pk>/', views.SensorUpdateView.as_view()),
    path('node/', views.SensorNode.as_view()),
    path('node/<int:pk>/', views.NodeDetail.as_view()),
    path('register/', views.SensorCreateView.as_view()),
    # path('powermon/data/', views.addItem)
]