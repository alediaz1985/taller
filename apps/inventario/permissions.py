# apps/inventario/permissions.py

from django.contrib.auth.models import User

def es_administrador(user):
    # Verifica si el usuario está autenticado y tiene permisos de administrador
    return user.is_authenticated and user.is_staff
