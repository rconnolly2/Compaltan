from django.shortcuts import render, redirect
from django.db.models import Q # Esto te permite puertas "and" "or" etc .. buscando datos
from django.http import HttpResponse
from django.contrib.auth.models import User # Importa usuario del MODEL
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required # Decorador de django para restringir paginas
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm # Nos facilita crear formulario para usuarios nuevos
from .models import Habitacion, Tema, Mensaje
from .forms import HabitacionForm, UsuarioForm
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
    mensajes_habitacion = Mensaje.objects.filter(Q(habitacion__nombre__icontains=q)).order_by("-created")
    
    contexto = {"rooms": rooms, "temas": temas, "numero_habitaciones": numero_habitaciones, "request": request, "mensajes_habitacion": mensajes_habitacion}
    return render(request, "home.html", contexto)

def room(request, pk):
    room = Habitacion.objects.get(id=pk)
    mensajes = room.mensaje_set.all().order_by("-created") #_set.all() coge todos los comentarios
    participantes = room.participantes.all()


    if request.method == "POST":
        mensaje = Mensaje.objects.create(usuario=request.user, habitacion=room, body=request.POST.get("body"))
        room.participantes.add(request.user)
        return redirect("room", pk=room.id) #Redirecciona con su pk

    contexto = {"room": room, "mensajes": mensajes, "request": request, "participantes": participantes}

    #return HttpResponse("Habitacion")
    return render(request, "room.html", contexto)


def PerfilUsuario(request, pk):
    usuario = User.objects.get(id=pk)
    mensaje_habitacion = usuario.mensaje_set.all()
    temas = Tema.objects.all()
    habitaciones = usuario.habitacion_set.all() #Me da todas las propiedades de habitacion => del usuario

    contexto = {"usuario": usuario, "rooms": habitaciones, "mensajes_habitacion": mensaje_habitacion, "temas": temas}
    return render(request, "perfil.html", contexto)


@login_required(login_url="login-page") # Decorador que restringe acceso y redirecciona a login
def createroom(request):
    form = HabitacionForm()
    temas = Tema.objects.all()

    contexto = {"form": form, "temas": temas}

    if request.method == "POST":
        tema_nombre = request.POST.get("tema")
        tema, creado = Tema.objects.get_or_create(nombre=tema_nombre)

        Habitacion.objects.create(host=request.user, tema=tema, nombre=request.POST.get("nombre"), descripcion=request.POST.get("descripcion"))
        return redirect("home")
        #form = HabitacionForm(request.POST)
        '''if form.is_valid() == True:
            room = form.save(commit=False)
            room.host = request.user # Pongo desde el server que el que envie el formulario es el host de Habitacion
            room.save()'''
            #return redirect("home")


    return render(request, "room_form.html", contexto)

@login_required(login_url="login-page") # Decorador que restringe acceso y redirecciona a login
def actualizarHabitacion(request, pk):
    room = Habitacion.objects.get(id=pk)
    form = HabitacionForm(instance=room)
    temas = Tema.objects.all()

    if not (request.user == room.host):
        return HttpResponse("Tu no estas permitido aqui !") #Que es request.user https://stackoverflow.com/questions/17312831/what-does-request-user-refer-to-in-django

    if request.method == "POST":
        #form = HabitacionForm(request.POST, instance=room)
        tema_nombre = request.POST.get("tema")
        tema, creado = Tema.objects.get_or_create(nombre=tema_nombre)
        room.nombre = request.POST.get("nombre")
        room.tema = tema
        room.descripcion = request.POST.get("descripcion")
        room.save()
        return redirect("home")

    contexto = {"form": form, "temas": temas, "room": room}

    return render(request, "room_form.html", contexto)

@login_required(login_url="login-page") # Decorador que restringe acceso y redirecciona a login
def eliminarHabitacion(request, pk):

    room = Habitacion.objects.get(id=pk)
    contexto = {"obj": room}
    if request.method == "POST":
        room.delete()
        return redirect("home")

    return render(request, "eliminar.html", contexto)

@login_required(login_url="login-page") # Decorador que restringe acceso y redirecciona a login
def eliminarMensaje(request, pk):

    mensaje = Mensaje.objects.get(id=pk)

    if request.user != mensaje.usuario:
        return HttpResponse("No estas permitido aqui !")


    if request.method == "POST":
        mensaje.delete()
        return redirect("home")
    
    contexto = {"obj": mensaje}
    return render(request, "eliminar.html", contexto)


@login_required(login_url="login-page") # Decorador que restringe acceso y redirecciona a login
def EditarUsuario(request, pk):
    usuario = request.user
    formulario = UsuarioForm(instance=usuario)

    if request.method == "POST":
        formulario = UsuarioForm(request.POST, instance=usuario)
        if formulario.is_valid() == True:
            formulario.save()
            return redirect("perfil-usuario", pk=usuario.id)

    contexto = {"formulario": formulario}
    return render(request, "editar-usuario.html", contexto)