from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.ClientsList.as_view()),
    path('list/<int:pk>/remo_scs_cpf/', views.RemoStartChargeView.as_view()),
    path('list/<int:pk>/remo_stop_cs/', views.RemoStopChargeView.as_view()),
    path('list/<int:pk>/reset/', views.ClientsResetView.as_view()),
    # path('list/<int:pk>/', views.ClientsDetail.as_view()),
    # path('update/<int:pk>/', views.ClientsUpdateView.as_view()),
    # path('node/', views.ClientsNode.as_view()),
    # path('node/<int:pk>/', views.NodeDetail.as_view()),
    # path('register/', views.ClientsCreateView.as_view()),
]