# apps/soporte/views.py
from django.shortcuts import render

def index(request):
    return render(request, 'soporte/index.html')
