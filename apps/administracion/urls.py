# apps/administracion/urls.py
from django.urls import path
from . import views  # Importa las vistas del mismo módulo
from .views import contacto_view

app_name = 'administracion'  # Define el namespace para la aplicación

urlpatterns = [
    path('', views.index_global, name='index_global'),
    path('administracion/', views.index, name='index'),  # Ruta para la vista de la aplicación # Ruta para la vista de la aplicación
    path('contacto/', contacto_view, name='contacto'), 
]


