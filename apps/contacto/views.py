from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from .forms import ContactoForm
import logging

logger = logging.getLogger(__name__)

def contacto_view(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data.get('phone', 'No proporcionado')
            message = form.cleaned_data['message']

            message_body = f"Nombre: {name}\nCorreo: {email}\nTeléfono: {phone}\n\nMensaje:\n{message}"

            try:
                send_mail(
                    subject=f"Mensaje de {name}",
                    message=message_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
                enviado = True
            except Exception as e:
                logger.error(f"Error al enviar el correo: {e}")
                enviado = False

            return render(request, 'contacto/confirmacion_contacto.html', {
                'enviado': enviado,
                'nombre': name
            })
    else:
        form = ContactoForm()

    return render(request, 'contacto/contacto.html', {'form': form})
