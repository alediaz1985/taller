from django import forms
from .models import Turno

"""class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['fecha_turno', 'numero_dominio', 'apellido', 'nombre', 'modelo_vehiculo', 'localidad', 'telefono']
"""

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['fecha_turno', 'numero_dominio', 'apellido', 'nombre', 'modelo_vehiculo', 'localidad', 'telefono']
        widgets = {
            'fecha_turno': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'numero_dominio': forms.TextInput(attrs={'placeholder': 'Ej: ABC123'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Ej: 3644...'}),
        }
