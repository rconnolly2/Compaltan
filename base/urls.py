from django.urls import path
from . import views #Importo el arhivo views.py de mi directorio



urlpatterns = [
    path("", views.home, name="home"),
    path("room/<str:pk>", views.room, name="room"), ## <str:pki> el tipo de dato del parametro en este caso int y lo guardamos en la variable pki 
    path("create-room/", views.createroom, name="create-room"),
    path("update-room/<str:pk>", views.actualizarHabitacion, name="update-room"),
    path("eliminar-room/<str:pk>", views.eliminarHabitacion, name="eliminar-room"),
    path("login-page/", views.loginPage, name="login-page"),
    path("logout-page/", views.logOut, name="logOut"),
    path("registrar-usuario/", views.registrarUsuario, name="registrarUsuario"),
    path("eliminar-mensaje/<str:pk>", views.eliminarMensaje, name="eliminar-mensaje"),
    path("perfil/<str:pk>", views.PerfilUsuario, name="perfil-usuario"),
]