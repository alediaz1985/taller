from django import forms

class RutaBusquedaForm(forms.Form):
    directorio_busqueda = forms.CharField(
        label='Ruta base',
        max_length=255,
        required=True
    )
    nombre_archivo = forms.CharField(
        label='Nombre del archivo (opcional)',
        max_length=255,
        required=False
    )
    fecha_desde = forms.DateField(
        label='Fecha desde (opcional)',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    fecha_hasta = forms.DateField(
        label='Fecha hasta (opcional)',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
