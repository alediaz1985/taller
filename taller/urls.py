# taller/urls.py
from django.contrib import admin
from django.urls import path, include
from apps.administracion.views import index_global
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_global, name='index_global'),  # Ruta principal
    path('authturno/', include('apps.authturno.urls')),  # Incluye las URLs de discapacidad
    path('discapacidad/', include('apps.discapacidad.urls')),  # Incluye las URLs de discapacidad
    path('excombatiente/', include('apps.excombatiente.urls')), #Incluye las URLs de Excombatiente
    path('mantenimiento/', include('apps.mantenimiento.urls')), #Incluye las URLs de Mantenimiento
    path('inventario/', include('apps.inventario.urls')), #Incluye las URLs de Inventario
    #path('usuarios/', include('apps.usuarios.urls')),
    path('administracion/', include('apps.administracion.urls')),  # Incluye las URLs de administracion
    path('notificaciones/', include('apps.notificaciones.urls')),
    path('pagos/', include('apps.pagos.urls')),
    path('cedulas/', include('apps.cedulas.urls', namespace='cedulas')),
    path('contacto/', include('apps.contacto.urls', namespace='contacto')),
    path('soporte/', include('apps.soporte.urls')),
    path('turnos/', include('apps.turnos.urls')),
    path('accounts/', include('apps.usuarios.urls')),
    path('archivos/', include('apps.buscadorpdf.urls', namespace='buscadorpdf')),
] + static(settings.CEDULAS_URL, document_root=settings.CEDULAS_DIR)