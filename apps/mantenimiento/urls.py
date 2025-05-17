# apps/mantenimiento/urls.py

from django.urls import path
from . import views

app_name = 'mantenimiento'

urlpatterns = [
    path('registrar/', views.registrar_mantenimiento, name='registrar_mantenimiento'),  # Ruta para registrar mantenimientos
    path('consulta/', views.consulta_mantenimientos, name='consulta_mantenimientos'),  # Esta debe ser la ruta correcta
    path('reporte/', views.generar_pdf, name='generar_pdf'),
   ]
