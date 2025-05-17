# apps/excombatiente/urls.py
from django.urls import path
from . import views

app_name = 'excombatiente'

urlpatterns = [
    path('', views.index, name='index'),
]