# apps/cedulas/forms.py
from django import forms
from .models import Cedula

class CedulaForm(forms.ModelForm):
    class Meta:
        model = Cedula
        fields = ['dominio', 'observaciones']

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Seteamos el campo que se está guardando para el nombre del archivo
        instance._upload_campo = 'frente'
        frente = self.cleaned_data['frente']
        instance.frente.save(frente.name, frente, save=False)

        instance._upload_campo = 'dorso'
        dorso = self.cleaned_data['dorso']
        instance.dorso.save(dorso.name, dorso, save=False)

        if commit:
            instance.save()
        return instance
