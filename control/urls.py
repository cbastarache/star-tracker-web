from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('getPorts', views.getPorts),
    path('connect', views.connect),
    path('disconnect', views.disconnect),
    path('sendCmd', views.sendCommand),
    path('sendData', views.sendData),
    path('status', views.status),
    path('objects', views.objectspage),
    path('addobject', views.addObject),
    path('track', views.track),
    path('setTLE', views.quicktrack),
]