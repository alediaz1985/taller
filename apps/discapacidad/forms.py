# apps/discapacidad/forms.py

from django import forms
from .models import Discapacitado, Tutor
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class DiscapacitadoForm(forms.ModelForm):
    menor_edad = forms.BooleanField(label="Es Menor de Edad", required=False)

    class Meta:
        model = Discapacitado
        fields = [
            'dni', 'apellido', 'nombre', 'direccion', 'telefono', 
            'numero_patente', 'tutor_dni', 'tutor_apellido', 
            'tutor_nombre', 'tutor_relacion'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if len(str(dni)) != 8:
            raise forms.ValidationError("El DNI debe tener exactamente 8 dígitos.")
        return dni

    def clean_numero_patente(self):
        numero_patente = self.cleaned_data.get('numero_patente')
        # Agrega aquí más validaciones si es necesario
        return numero_patente

class TutorForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = ['dni', 'apellido', 'nombre', 'relacion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if len(str(dni)) != 8:
            raise ValidationError("El DNI debe tener exactamente 8 dígitos.")
        return dni

class ConsultaForm(forms.Form):
    dni = forms.CharField(
        label='DNI', 
        max_length=8, 
        required=False,
        validators=[
            RegexValidator(regex='^\d{1,8}$', message='Ingrese un DNI válido con hasta 8 dígitos numéricos.')
        ],
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese DNI', 'class': 'form-control'})
    )
    numero_patente = forms.CharField(
        label='Número de Patente', 
        max_length=10, 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese Número de Patente', 'class': 'form-control'})
    )

class AsistenciaForm(forms.Form):
    dni = forms.IntegerField(label='DNI', required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    numero_patente = forms.CharField(label='Número de Patente', max_length=10, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
