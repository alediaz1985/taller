from django import forms
from .models import Turno

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['nombre', 'apellido', 'dni_cuit', 'telefono', 'correo', 'dominio', 'fecha', 'hora']
