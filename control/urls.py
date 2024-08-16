from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('getPorts', views.getPorts),
    path('connect', views.connect),
    path('sendCmd', views.sendCommand),
    path('status', views.status),
]