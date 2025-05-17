from django.contrib import admin

# Register your models here.
from .models import TipoBien



@admin.register(TipoBien)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ['nombre']  # Asegúrate de que estos campos existan en Equipo
    search_fields = ['nombre']  # Opcional, para agregar búsqueda
