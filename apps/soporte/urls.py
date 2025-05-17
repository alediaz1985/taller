# apps/soporte/urls.py
from django.urls import path
from . import views
app_name = 'soporte'
urlpatterns = [
    path('', views.index, name='index'),
    # Agrega otras rutas aquí según las vistas que tengas en `views.py`
]
