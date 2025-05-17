from django.contrib import admin
from apps.inventario.models import Equipo  # Asegúrate de importar el modelo correcto desde inventario
from .models import TipoTrabajo, Mantenimiento

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ['codigo_interno', 'tipo_bien', 'marca', 'modelo']  # Asegúrate de que estos campos existan en Equipo
    search_fields = ['codigo_interno', 'marca', 'modelo']  # Opcional, para agregar búsqueda

@admin.register(TipoTrabajo)
class TipoTrabajoAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']

@admin.register(Mantenimiento)
class MantenimientoAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'equipo', 'tipo_trabajo', 'responsable']
    search_fields = ['equipo__codigo_interno', 'tipo_trabajo__nombre', 'responsable__username']
    list_filter = ['fecha', 'equipo', 'tipo_trabajo', 'responsable']
