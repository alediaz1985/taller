# apps/discapacidad/models.py

from django.db import models
from django.utils import timezone

class Discapacitado(models.Model):
    dni = models.CharField(max_length=8, primary_key=True)
    apellido = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    numero_patente = models.CharField(max_length=10, unique=True)
    tutor_dni = models.CharField(max_length=8, null=True, blank=True)
    tutor_apellido = models.CharField(max_length=100, null=True, blank=True)
    tutor_nombre = models.CharField(max_length=100, null=True, blank=True)
    tutor_relacion = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Asistencia(models.Model):
    discapacitado = models.ForeignKey(Discapacitado, on_delete=models.CASCADE, related_name='asistencias')
    fecha_asistencia = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return f"Asistencia: {self.discapacitado} en {self.fecha_asistencia}"

class Tutor(models.Model):
    dni = models.IntegerField(primary_key=True)
    apellido = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    relacion = models.CharField(max_length=100)
    discapacitado = models.ForeignKey(Discapacitado, on_delete=models.CASCADE, related_name='tutores')

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.relacion}"
