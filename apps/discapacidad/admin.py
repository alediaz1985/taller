from django.contrib import admin
from .models import Discapacitado, Tutor, Asistencia

admin.site.register(Discapacitado)
admin.site.register(Asistencia)
admin.site.register(Tutor)