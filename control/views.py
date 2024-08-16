from django.shortcuts import render
from django.http import HttpResponse
import startracker.settings
import json

def index(request):
    return render(request, "control.html")

def getPorts(request):
    ports = startracker.settings.serial.getPorts()
    print(ports)
    return HttpResponse(json.dumps(ports))

def connect(request):
    startracker.settings.serial.openPort(request.GET["port"])
    return HttpResponse("OK")

def sendCommand(request):
    startracker.settings.serial.write(request.GET["cmd"])
    return HttpResponse("OK")

def status(request):
    startracker.settings.serial.write("POS")
    data = startracker.settings.serial.read()
    print(data)
    return HttpResponse(data)
