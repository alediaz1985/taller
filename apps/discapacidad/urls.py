# apps/discapacidad/urls.py

from django.urls import path
from . import views

app_name = 'discapacidad'

urlpatterns = [
    path('', views.index, name='index'),
    path('verificar/', views.verificar, name='verificar'),
    path('consulta/', views.consulta_discapacitado, name='consulta'),
    path('registrar_nuevo/', views.registrar_nuevo, name='registrar_nuevo'),
    path('registrar_asistencia/', views.registrar_asistencia, name='registrar_asistencia'),
    path('registrar_visita/<int:dni>/', views.registrar_visita, name='registrar_visita'),
]