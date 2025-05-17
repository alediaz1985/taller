from django.contrib import admin
from .models import Turno

@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ('numero_dominio', 'apellido', 'nombre', 'modelo_vehiculo', 'localidad', 'telefono', 'fecha_turno')  # Campos que deseas mostrar
    search_fields = ('numero_dominio', 'apellido')  # Campos para búsqueda
    list_filter = ('fecha_turno',)  # Filtros laterales opcionales
