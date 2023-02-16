from django.forms import ModelForm
from .models import Habitacion, User
from django.contrib.auth.forms import UserCreationForm

class HabitacionForm(ModelForm):
    class Meta:
        model = Habitacion
        fields = "__all__" ## o danos datos especificios como : ["nombre, "id" ...]
        exclude = ["host", "participantes"] # Aqui ponemos las propiedades de Habitacion que quiero excluir

class UsuarioForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "name", "avatar", "biografia"]


class FormularioCrearUsuario(UserCreationForm):
    class Meta:
        model = User
        fields = ["name", "username", "email", "password1", "password2"]