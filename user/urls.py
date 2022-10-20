from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index),
    path('list/', views.UserList.as_view()),
    path('register/', views.UserCreateView.as_view()),
    # path('powermon/data/', views.addItem)
]