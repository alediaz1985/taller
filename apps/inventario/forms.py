from django import forms
from .models import Equipo, HistorialBaja, TipoBien

class TipoBienForm(forms.ModelForm):
    class Meta:
        model = TipoBien
        fields = ['nombre', 'prefijo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'prefijo': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if TipoBien.objects.filter(nombre=nombre).exists():
            raise forms.ValidationError("Este tipo de bien ya está registrado.")
        return nombre




class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ['codigo_interno', 'tipo_bien', 'marca', 'modelo', 'numero_serie', 'fecha_compra']
        labels = {
            'codigo_interno': 'Código Interno',
            'tipo_bien': 'Tipo de Bien',
            'marca': 'Marca',
            'modelo': 'Modelo',
            'numero_serie': 'Número de Serie',
            'fecha_compra': 'Fecha de Compra',
        }
        widgets = {
            'codigo_interno': forms.TextInput(attrs={'readonly': 'readonly'}),  # Campo de solo lectura
            'fecha_compra': forms.DateInput(attrs={'type': 'date'}),  # Selector de fecha en el calendario
        }

class BajaForm(forms.ModelForm):
    class Meta:
        model = HistorialBaja
        fields = ['motivo']
        labels = {
            'motivo': 'Motivo de Baja',
        }
