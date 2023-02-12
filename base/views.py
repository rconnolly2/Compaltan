from django.shortcuts import render, redirect
from django.db.models import Q # Esto te permite puertas "and" "or" etc .. buscando datos
from django.http import HttpResponse
from .models import Habitacion, Tema
from .forms import HabitacionForm
# Create your views here.

'''rooms = [{"id": 1, "name": "Me gusta python !"},
         {"id": 2, "name": "Me gusta C++ !"},
         {"id": 3, "name": "Me gusta DJANGO Framework !"}]'''

def home(request):

    if not request.GET.get("q") == None:
        q = request.GET.get("q")
    else:
        q = ""

    temas = Tema.objects.all()
    rooms = Habitacion.objects.filter(Q(tema__nombre__icontains=q) | Q(descripcion__icontains=q) | Q(nombre__icontains=q)) # Q te permite poner varios parametros 
    contexto = {"rooms": rooms, "temas": temas}
    return render(request, "home.html", contexto)

def room(request, pk):
    room = Habitacion.objects.get(id=pk)

    contexto = {"room": room}

    #return HttpResponse("Habitacion")
    return render(request, "room.html", contexto)

def createroom(request):
    form = HabitacionForm()
    contexto = {"form": form}

    if request.method == "POST":
        print(request.POST)
        form = HabitacionForm(request.POST)
        if form.is_valid() == True:
            form.save()
            return redirect("home")


    return render(request, "room_form.html", contexto)


def actualizarHabitacion(request, pk):
    room = Habitacion.objects.get(id=pk)
    form = HabitacionForm(instance=room)

    if request.method == "POST":
        form = HabitacionForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")

    contexto = {"form": form}

    return render(request, "room_form.html", contexto)


def eliminarHabitacion(request, pk):

    room = Habitacion.objects.get(id=pk)
    contexto = {"obj": room}
    if request.method == "POST":
        room.delete()
        return redirect("home")

    return render(request, "eliminar.html", contexto)