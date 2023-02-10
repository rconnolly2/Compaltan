from django.shortcuts import render
from django.http import HttpResponse
from .models import Habitacion
# Create your views here.

rooms = [{"id": 1, "name": "Me gusta python !"},
         {"id": 2, "name": "Me gusta C++ !"},
         {"id": 3, "name": "Me gusta DJANGO Framework !"}]

def home(request):
    rooms = Habitacion.objects.all()
    contexto = {"rooms": rooms}
    return render(request, "home.html", contexto)

def room(request, pk):
    room = None

    for i in rooms:
        if i["id"] == int(pk):
            room = i

    contexto = {"room": room}

    #return HttpResponse("Habitacion")
    return render(request, "room.html", contexto)