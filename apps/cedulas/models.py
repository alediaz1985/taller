# apps/cedulas/models.py
import os
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

def ruta_archivo(instance, filename):
    # filename es tipo str (nombre original del archivo)
    fecha = datetime.now().strftime("%d%m%Y")
    dominio = instance.dominio.upper()
    
    # Detectar si es para el campo frente o dorso
    campo_llamador = ''
    if hasattr(instance, '_upload_campo'):
        campo_llamador = instance._upload_campo

    tipo = 'F' if campo_llamador == 'frente' else 'D'
    extension = os.path.splitext(filename)[1]

    nuevo_nombre = f"{dominio}_{tipo}{fecha}{extension}"
    return f"apps/cedulas/media/{dominio}/{nuevo_nombre}"


"""class Cedula(models.Model):
    dominio = models.CharField(max_length=10)
    frente = models.ImageField(upload_to=ruta_archivo)
    dorso = models.ImageField(upload_to=ruta_archivo)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.dominio} - {self.fecha_subida.strftime('%d/%m/%Y %H:%M')}"""



class Cedula(models.Model):
    dominio = models.CharField(max_length=10)
    ruta_pdf = models.TextField(null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True) 
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.dominio.upper()} - {self.fecha_subida.strftime('%d/%m/%Y %H:%M')}"
