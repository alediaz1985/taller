# apps/notificaciones/views.py
from django.shortcuts import render

def index(request):
    return render(request, 'notificaciones/index.html')
