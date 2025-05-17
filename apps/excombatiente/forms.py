from django import forms

class ConsultaDNIForm(forms.Form):
    dni = forms.CharField(label='DNI', max_length=10)