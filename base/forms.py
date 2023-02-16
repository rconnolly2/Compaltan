from django.forms import ModelForm
from .models import Habitacion
from django.contrib.auth.models import User


class HabitacionForm(ModelForm):
    class Meta:
        model = Habitacion
        fields = "__all__" ## o danos datos especificios como : ["nombre, "id" ...]
        exclude = ["host", "participantes"] # Aqui ponemos las propiedades de Habitacion que quiero excluir

class UsuarioForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]