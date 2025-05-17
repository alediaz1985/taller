# apps/mantenimiento/forms.py

from django import forms
from .models import Mantenimiento, TipoTrabajo
from apps.inventario.models import Equipo  # Importamos Equipo desde inventario

class MantenimientoForm(forms.ModelForm):
    class Meta:
        model = Mantenimiento
        fields = ['equipo', 'tipo_trabajo', 'observaciones']
        labels = {
            'equipo': 'Equipo',
            'tipo_trabajo': 'Tipo de Trabajo',
            'observaciones': 'Observaciones',
        }

class TipoTrabajoForm(forms.ModelForm):
    class Meta:
        model = TipoTrabajo
        fields = ['nombre']
        labels = {
            'nombre': 'Nombre del Tipo de Trabajo',
        }

class ConsultaMantenimientoForm(forms.Form):
    fecha_inicio = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    fecha_fin = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    equipo = forms.ModelChoiceField(queryset=Equipo.objects.all(), required=False, label='Equipo')
