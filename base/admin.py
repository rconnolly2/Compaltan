from django.contrib import admin

# Register your models here.
from .models import Habitacion, Tema, Mensaje, User

admin.site.register(Habitacion)
admin.site.register(Tema)
admin.site.register(Mensaje)
admin.site.register(User)