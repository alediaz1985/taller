# apps/mantenimiento/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from apps.inventario.models import Equipo  # Importa Equipo desde inventario

class TipoTrabajo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Mantenimiento(models.Model):
    fecha = models.DateTimeField(default=timezone.now)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    tipo_trabajo = models.ForeignKey(TipoTrabajo, on_delete=models.CASCADE)
    observaciones = models.TextField(blank=True, null=True)
    responsable = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.fecha} - {self.equipo}"
