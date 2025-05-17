from django.db import models

class Turno(models.Model):
    VEHICULOS = [
        ('gol', 'Gol'),
        ('voyage', 'Voyage'),
        ('aveo', 'Aveo'),
        ('prisma', 'Prisma'),
        ('suran', 'Suran'),
        ('206', 'Peugeot 206'),
        ('207', 'Peugeot 207'),
        ('208', 'Peugeot 208'),
        ('307', 'Peugeot 307'),
        ('ecosport', 'Ecosport'),
        ('audi_a5', 'Audi A5'),
        ('408', 'Peugeot 408'),
        ('508', 'Peugeot 508'),
        ('hilux', 'Hilux'),
        ('corolla', 'Corolla'),
    ]

    LINEAS = [
        ('livianos', 'Línea Livianos'),
        ('mixta', 'Línea Mixta'),
    ]

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni_cuit = models.CharField(max_length=15)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()
    dominio = models.CharField(max_length=10, unique=True)
    vehiculo = models.CharField(max_length=50, choices=VEHICULOS)
    linea = models.CharField(max_length=10, choices=LINEAS, editable=False)
    fecha = models.DateField()
    hora = models.TimeField()
    reservado = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Determinar la línea automáticamente según el vehículo
        if self.vehiculo in ['gol', 'voyage', 'aveo', 'prisma', 'suran', '206', '207', '208', '307', 'audi_a5']:
            self.linea = 'livianos'
        elif self.vehiculo in ['408', '508', 'ecosport', 'hilux', 'corolla']:
            self.linea = 'mixta'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.fecha} {self.hora} ({self.linea})"
