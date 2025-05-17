from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
import os
import random
from django.conf import settings

from django.core.mail import send_mail
from django.http import HttpResponse
from .forms import ContactoForm

from django.contrib import messages  # Para los mensajes de éxito
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


"""
funciona pero no redirije y no manda número de telefonos
def contacto_view(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            # Recoger los datos del formulario
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            message = form.cleaned_data['message']

            # Enviar un correo electrónico
            send_mail(
                f'Mensaje de {name}',
                message,
                email,
                [settings.CONTACT_EMAIL],  # Define un correo de recepción en settings
                fail_silently=False,
            )
            return HttpResponse('Gracias por tu mensaje.')
    else:
        form = ContactoForm()

    return render(request, 'administracion/contacto.html', {'form': form})
"""

def contacto_view(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            # Recoger los datos del formulario
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data.get('phone', 'No proporcionado')  # Si no se proporciona, usar un texto por defecto
            message = form.cleaned_data['message']

            # Crear el cuerpo del mensaje para incluir el teléfono
            message_body = f"Nombre: {name}\nCorreo: {email}\nTeléfono: {phone}\n\nMensaje:\n{message}"

            # Enviar un correo electrónico
            send_mail(
                f'Mensaje de {name}',  # Asunto del correo
                message_body,          # Cuerpo del mensaje con los datos
                email,                 # Remitente
                [settings.CONTACT_EMAIL],  # Destinatario (definido en settings.py)
                fail_silently=False,
            )

            # Mostrar mensaje de éxito
            messages.success(request, 'Tu mensaje ha sido enviado exitosamente. Le responderemos a la brevedad.')

            # Limpiar los mensajes después de mostrarlos
            storage = get_messages(request)
            for _ in storage:
                pass  # Esto fuerza a que los mensajes se consuman

            # Mostrar la página de confirmación
            return render(request, 'administracion/confirmacion_contacto.html')  # Nueva página de confirmación
    else:
        form = ContactoForm()

    return render(request, 'administracion/contacto.html', {'form': form})
