from django.shortcuts import render, redirect
from django.db.models import Q # Esto te permite puertas "and" "or" etc .. buscando datos
from django.http import HttpResponse
from django.contrib.auth.models import User # Importa usuario del MODEL
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required # Decorador de django para restringir paginas
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm # Nos facilita crear formulario para usuarios nuevos
from .models import Habitacion, Tema
from .forms import HabitacionForm
# Create your views here.

'''rooms = [{"id": 1, "name": "Me gusta python !"},
         {"id": 2, "name": "Me gusta C++ !"},
         {"id": 3, "name": "Me gusta DJANGO Framework !"}]'''

def logOut(request):

    logout(request)
    return redirect("home")

def registrarUsuario(request):
    pagina = "registrar"
    formulario = UserCreationForm()

    if request.method == "POST":
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid() == True:
            usuario = formulario.save(commit=False)
            usuario.username = usuario.username.lower()
            usuario.save()
            login(request, usuario)
            return redirect("home")
        else:
            messages.error(request, "Hubo un error al registrarse!")
    
    contexto = {"pagina": pagina, "formulario": formulario}
    return render(request, "login-register.html", contexto)


def loginPage(request):
    pagina = "login"

    if request.user.is_authenticated:
        return redirect("home") #Si el usuario ya esta logueado y intenta entrar a la link /login/ le redireccionara


    if request.method == "POST":
        usuario = request.POST.get("usuario").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=usuario)
        except:
            messages.error(request, "Usuario no existe")

        user = authenticate(request, username=usuario, password=password)

        if not (user is None):
            login(request, user) # Si el objeto user NO esta vacio (porque la contraseña es valida)
            return redirect("home")
        else:
            messages.error(request, "Contraseña no es valida!")


    contexto = {"pagina": pagina}
    return render(request, "login-register.html", contexto)


def home(request):

    if not request.GET.get("q") == None:
        q = request.GET.get("q")
    else:
        q = ""

    temas = Tema.objects.all()
    rooms = Habitacion.objects.filter(Q(tema__nombre__icontains=q) | Q(descripcion__icontains=q) | Q(nombre__icontains=q)) # Q te permite poner varios parametros 
    numero_habitaciones = len(rooms)

    contexto = {"rooms": rooms, "temas": temas, "numero_habitaciones": numero_habitaciones, "request": request}
    return render(request, "home.html", contexto)

def room(request, pk):
    room = Habitacion.objects.get(id=pk)

    contexto = {"room": room}

    #return HttpResponse("Habitacion")
    return render(request, "room.html", contexto)


@login_required(login_url="login-page") # Decorador que restringe acceso y redirecciona a login
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

@login_required(login_url="login-page") # Decorador que restringe acceso y redirecciona a login
def actualizarHabitacion(request, pk):
    room = Habitacion.objects.get(id=pk)
    form = HabitacionForm(instance=room)

    if not (request.user == room.host):
        return HttpResponse("Tu no estas permitido aqui !") #Que es request.user https://stackoverflow.com/questions/17312831/what-does-request-user-refer-to-in-django

    if request.method == "POST":
        form = HabitacionForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")

    contexto = {"form": form}

    return render(request, "room_form.html", contexto)

@login_required(login_url="login-page") # Decorador que restringe acceso y redirecciona a login
def eliminarHabitacion(request, pk):

    room = Habitacion.objects.get(id=pk)
    contexto = {"obj": room}
    if request.method == "POST":
        room.delete()
        return redirect("home")

    return render(request, "eliminar.html", contexto)