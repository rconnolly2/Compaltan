from django.forms import ModelForm
from .models import Habitacion

class HabitacionForm(ModelForm):
    class Meta:
        model = Habitacion
        fields = "__all__" ## o danos datos especificios como : ["nombre, "id" ...]
