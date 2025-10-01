import os
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

import random
from django.conf import settings

from django.core.mail import send_mail
from django.http import HttpResponse

from django.contrib import messages
from django.contrib.messages import get_messages

from django.utils.decorators import method_decorator

@login_required
def index_global(request):
    # Ruta completa donde se encuentran los archivos PDF
    pdf_directory = os.path.join(settings.BASE_DIR, 'taller', 'static', 'pdfs')
    
    # Verificar si la carpeta existe
    if not os.path.exists(pdf_directory):
        # Crear la carpeta si no existe (opcional)
        os.makedirs(pdf_directory)
        # O manejar el error adecuadamente, por ejemplo:
        return render(request, 'index.html', {
            'title': 'Inicio',
            'error_message': 'No se encontraron archivos PDF en la ubicación especificada.'
        })

    # Listar todos los archivos PDF en la carpeta
    pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
    
    # Generar la lista de URLs para los PDFs
    pdf_urls = [os.path.join('pdfs', pdf) for pdf in pdf_files]
    
    # Mezclar aleatoriamente la lista de PDFs
    random.shuffle(pdf_urls)

    context = {
        'title': 'Inicio',
        'pdf_urls': pdf_urls
    }
    
    return render(request, 'index.html', context)


@login_required
def index(request):
    context = {'title': 'Administración'}
    return render(request, 'administracion/index.html',context)