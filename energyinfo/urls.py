from django.urls import path
from . import views
from . import dashboard

urlpatterns = [
    path('list/', views.EnergyinfoList.as_view()),
    path('list/<int:pk>/', views.EnergyinfoDetail.as_view()),
    path('register/', views.EnergyinfoCreateView.as_view()),
    path('update/<int:pk>/', views.EnergyinfoUpdateView.as_view()),
    path('dashboard/', views.dashboard),
    path('fetch_sensor_values_ajax', dashboard.fetch_sensor_values_ajax, name='fetch_sensor_values_ajax'),
    path('schedulemail/', views.schedule_mail, name='schedulemail'),
]