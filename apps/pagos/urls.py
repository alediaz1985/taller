# apps/pagos/urls.py
from django.urls import path
from . import views

app_name = 'pagos'  # Define el namespace para la aplicación

urlpatterns = [
    path('', views.index, name='index'),
    # Agrega otras rutas aquí según las vistas que tengas en `views.py`
]
