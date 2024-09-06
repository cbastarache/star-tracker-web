from django.shortcuts import render
from django.http import HttpResponse
from control.models import Satellite
from control.CommandClient.client import Client
import startracker.settings
import json

def index(request):
    s = Satellite.objects.all()
    context = {
        "port_list": startracker.settings.serial.getPorts(),
        "connected": startracker.settings.serial.connectedPort,
        "tracking" : "",
        "object_list": s,

    }
    return render(request, "control.html", context)

def getPorts(request):
    ports = startracker.settings.serial.getPorts()
    print(ports)
    return HttpResponse(json.dumps(ports))

def connect(request):
    startracker.settings.serial.openPort(request.GET["port"])
    return HttpResponse("OK")

def disconnect(request):
    startracker.settings.serial.close()
    return HttpResponse("OK")

def sendCommand(request):
    startracker.settings.serial.write(request.GET["cmd"])
    return HttpResponse("OK")

def status(request):
    startracker.settings.serial.write("POS")
    data = startracker.settings.serial.read()
    print(data)
    return HttpResponse(data)

def objectspage(request):
    s = Satellite.objects.all()
    context = {
        "object_list": s
    }
    return render(request, "objects.html", context)

def addObject(request):
    if request.method == "POST":
        data = request.POST
        print(data['noradID'])
        try:
            existingObj = Satellite.objects.get(catNo=data['noradID'])
        except:
            newObj = Satellite(
                catNo = int(data['noradID']),
                name = data['name'],
                tle1 = data['tle1'],
                tle2 = data['tle2'],
                uplink = float(data['uplink']),
                downlink = float(data['downlink']),
                classification = ""
            )
            newObj.save()

    return render(request, "addobject.html")

def sCallback(data):
    print(data)

def track(request):
    o = Satellite.objects.get(catNo=request.GET["ID"])
    payload = {
        "tle1": o.tle1,
        "tle2": o.tle2,
    }
    client = Client("127.0.0.1", 5411, sCallback)
    client.sendMessage(payload)
    return HttpResponse("OK")

def quicktrack(request):
    payload = {
        "tle1": request.GET["tle1"],
        "tle2": request.GET["tle2"],
    }
    client = Client("127.0.0.1", 5411, sCallback)
    client.sendMessage(payload)
    return HttpResponse("OK")