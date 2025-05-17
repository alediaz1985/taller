from django.db import models

class Turno(models.Model):
    numero_dominio = models.CharField(max_length=10)
    apellido = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    modelo_vehiculo = models.CharField(max_length=50)
    localidad = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15)
    fecha_turno = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return f"{self.numero_dominio} - {self.apellido}, {self.nombre}"
