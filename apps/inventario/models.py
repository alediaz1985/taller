from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import Max

class TipoBien(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    prefijo = models.CharField(max_length=10, unique=True, default="codinterno")

    def __str__(self):
        return self.nombre

    def delete(self, *args, **kwargs):
        # Verifica si el tipo de bien tiene equipos asociados
        if self.equipos.exists():
            raise ValidationError("No se puede eliminar el Tipo de Bien porque tiene equipos asociados.")
        super().delete(*args, **kwargs)

class Equipo(models.Model):
    tipo_bien = models.ForeignKey(TipoBien, on_delete=models.CASCADE, related_name='equipos')
    codigo_interno = models.CharField(max_length=10, unique=True, blank=True)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    numero_serie = models.CharField(max_length=100)
    fecha_compra = models.DateField()
    activo = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Solo generar el código interno si el equipo es nuevo y no tiene uno
        if not self.codigo_interno:
            ultimo_equipo = Equipo.objects.filter(tipo_bien=self.tipo_bien).aggregate(Max('codigo_interno'))
            ultimo_codigo = ultimo_equipo['codigo_interno__max']
            
            if ultimo_codigo:
                # Extraer el número del último código
                ultimo_numero = int(ultimo_codigo.split('-')[1])
                nuevo_numero = ultimo_numero + 1
            else:
                # Si no hay equipos, empezar desde 1
                nuevo_numero = 1

            # Generar el nuevo código interno
            self.codigo_interno = f"{self.tipo_bien.prefijo}-{str(nuevo_numero).zfill(3)}"  # MON-001, MON-002, etc.
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codigo_interno} - {self.marca} {self.modelo}"

class HistorialBaja(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='historial_bajas')
    fecha_baja = models.DateField(default=timezone.now)
    motivo = models.TextField()
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Baja de {self.equipo.codigo_interno} - {self.fecha_baja}"
