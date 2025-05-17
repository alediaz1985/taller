from django.db import models

class ExCombatiente(models.Model):
    dni = models.CharField(max_length=10, unique=True)
    apellido_nombre = models.CharField(max_length=255)
    fuerza = models.CharField(max_length=100)
    grado = models.CharField(max_length=100)
    condicion = models.CharField(max_length=50)
    vive = models.BooleanField()

    def __str__(self):
        return f"{self.apellido_nombre} - {self.dni}"
