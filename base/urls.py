from django.urls import path
from . import views #Importo el arhivo views.py de mi directorio



urlpatterns = [
    path("", views.home, name="home"),
    path("room/<str:pk>", views.room, name="room"), ## <str:pki> el tipo de dato del parametro en este caso int y lo guardamos en la variable pki 
]