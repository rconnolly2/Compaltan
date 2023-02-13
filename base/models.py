from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Tema(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre



class Habitacion(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tema = models.ForeignKey(Tema, on_delete=models.SET_NULL, null=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(null=True, blank=True)
    #participantes = 
    updated = models.DateTimeField(auto_now=True)
    creado = models.DateTimeField(auto_now_add=True) #Este valor solo cambia cuando se INICIA UNA VEZ


    class Meta:
        ordering = ["-updated", "-creado"]

    def __str__(self):
        return self.nombre
    

    
class Mensaje(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    #Constructor
    def __str__(self):
        return self.body[0:50]