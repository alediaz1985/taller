import os
import json
from django.conf import settings
from django.core.wsgi import get_wsgi_application

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taller.settings')
application = get_wsgi_application()

from excombatiente.models import ExCombatiente

# Cargar datos del archivo JSON
with open('C:\\proyectos\\taller_entorno\\taller\\apps\\excombatiente\\veteranos.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    for item in data:
        ExCombatiente.objects.create(
            dni=item['Doc'],
            apellido_nombre=item['Apellido y Nombre'],
            fuerza=item['Fuerza'],
            grado=item['Grado en Conflicto'],
            condicion=item['Condición'],
            vive=True if item['Vive?'] == 'SI' else False
        )
