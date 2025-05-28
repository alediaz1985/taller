from django.urls import path
from .views import contacto_view

app_name = 'contacto'  # Define el namespace para la aplicación

urlpatterns = [
    path('', contacto_view, name='contacto'),
]
