from django.contrib import admin

# Register your models here.
from .models import Habitacion, Tema, Mensaje

admin.site.register(Habitacion)
admin.site.register(Tema)
admin.site.register(Mensaje)