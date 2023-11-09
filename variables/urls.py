from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index),
    # path('dashboard/', views.dashboard),
    path('list/', views.VariablesList.as_view()),
    path('register/', views.VariablesCreateView.as_view()),
    # path('powermon/data/', views.addItem)
]