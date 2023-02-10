from django.db import models

# Create your models here.
class Habitacion(models.Model):

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(null=True, blank=True)
    #participantes = 
    updated = models.DateTimeField(auto_now=True)
    creado = models.DateTimeField(auto_now_add=True) #Este valor solo cambia cuando se INICIA UNA VEZ

    def __str__(self):
        return self.nombre