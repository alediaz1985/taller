"""import os
from django.conf import settings  # Para obtener BASE_DIR
from django.shortcuts import render
from django.http import HttpResponse
from reportlab.lib.pagesizes import A5, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from io import BytesIO
from .forms import TurnoForm
from .models import Turno

def index(request):
    if request.method == 'POST':
        form = TurnoForm(request.POST)
        if form.is_valid():
            turno = form.save()

            # Generar PDF
            buffer = BytesIO()
            # Tamaño A5 en orientación horizontal
            page_width = 210 * mm  # 210mm (ancho en puntos)
            page_height = 148.5 * mm  # 148.5mm (alto en puntos)
            pdf = canvas.Canvas(buffer, pagesize=landscape((page_width, page_height)))

            # Ruta absoluta de la imagen
            background_image = os.path.join(settings.STATIC_BASE_PATH, 'background.png')

            print(f"Ruta de la imagen: {background_image}")
            try:
                # Ajustar la imagen al tamaño completo de la página
                pdf.drawImage(background_image, 0, 0, width=page_width, height=page_height, mask='auto')
            except OSError:
                pdf.drawString(10, page_height - 20, "Error: No se encontró la imagen de fondo")

            # Escribir datos en el PDF
            pdf.setFont("Helvetica", 12)

            pdf.drawString(20, page_height - 40, f"Dominio: {turno.fecha_turno}")
            pdf.drawString(20, page_height - 40, f"Dominio: {turno.numero_dominio}")
            pdf.drawString(20, page_height - 60, f"Apellido: {turno.apellido}")
            pdf.drawString(20, page_height - 80, f"Nombre: {turno.nombre}")
            pdf.drawString(20, page_height - 100, f"Modelo: {turno.modelo_vehiculo}")
            pdf.drawString(20, page_height - 120, f"Localidad: {turno.localidad}")
            pdf.drawString(20, page_height - 140, f"Teléfono: {turno.telefono}")

            # Guardar el PDF
            pdf.save()
            buffer.seek(0)

            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="turno.pdf"'
            return response
    else:
        form = TurnoForm()

    return render(request, 'authturno/index.html', {'form': form})
"""

import os
import qrcode
import tempfile  # Para archivos temporales
from django.conf import settings  # Para obtener BASE_DIR
from django.shortcuts import render
from django.http import HttpResponse
from reportlab.lib.pagesizes import A5, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from io import BytesIO
from .forms import TurnoForm
from .models import Turno

def index(request):
    if request.method == 'POST':
        form = TurnoForm(request.POST)
        if form.is_valid():
            turno = form.save()

            # Generar PDF
            buffer = BytesIO()
            # Tamaño A5 en orientación horizontal
            page_width = 210 * mm  # 210mm (ancho en puntos)
            page_height = 148.5 * mm  # 148.5mm (alto en puntos)
            pdf = canvas.Canvas(buffer, pagesize=landscape((page_width, page_height)))

            # Ruta absoluta de la imagen de fondo
            background_image = os.path.join(settings.STATIC_BASE_PATH, 'background.png')

            print(f"Ruta de la imagen: {background_image}")
            try:
                # Ajustar la imagen al tamaño completo de la página
                pdf.drawImage(background_image, 0, 0, width=page_width, height=page_height, mask='auto')
            except OSError:
                pdf.drawString(10, page_height - 20, "Error: No se encontró la imagen de fondo")

            # Datos fijos del taller
            datos_taller = {
                "Teléfono": "3644122222",
                "Dirección": "Ruta 16 Km 176 Pcia. Roque Sáenz Peña - Chaco",
                "Ubicación": "https://maps.app.goo.gl/9SiR6HWMGX2PxcNLA"
            }

            # Crear contenido para el código QR
            qr_data = (
                f"Fecha del turno: {turno.fecha_turno}\n"
                f"Dominio: {turno.numero_dominio}\n"
                f"Apellido: {turno.apellido}\n"
                f"Nombre: {turno.nombre}\n"
                f"Teléfono: {turno.telefono}\n"
                f"Modelo: {turno.modelo_vehiculo}\n"
                f"Localidad: {turno.localidad}\n"
                f"Taller: {datos_taller['Dirección']}, Tel: {datos_taller['Teléfono']}"
            )

            # Generar el código QR
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")

            # Guardar el QR como un archivo temporal
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
                qr_img.save(tmp_file, format="PNG")
                qr_path = tmp_file.name

            # Dibujar el QR en el PDF
            pdf.drawImage(qr_path, x=page_width - 70 * mm, y=30 * mm, width=50 * mm, height=50 * mm)

            # Escribir datos en el PDF
            pdf.setFont("Helvetica", 14)
            pdf.drawString(20, page_height - 180, f"Fecha del Turno: {turno.fecha_turno}")
            pdf.drawString(20, page_height - 200, f"Dominio: {turno.numero_dominio}")
            pdf.drawString(20, page_height - 220, f"Apellido: {turno.apellido}")
            pdf.drawString(20, page_height - 240, f"Nombre: {turno.nombre}")
            pdf.drawString(20, page_height - 260, f"Modelo: {turno.modelo_vehiculo}")
            pdf.drawString(20, page_height - 280, f"Localidad: {turno.localidad}")
            pdf.drawString(20, page_height - 300, f"Teléfono: {turno.telefono}")

            pdf.drawString(20, page_height - 320, f"Taller: {datos_taller['Dirección']}")

            # Escribir datos fijos del taller
            #pdf.drawString(20, 40, f"Teléfono del Taller: {datos_taller['Teléfono']}")
            #pdf.drawString(20, 20, f"Dirección: {datos_taller['Dirección']}")

            # Guardar el PDF
            pdf.save()
            buffer.seek(0)

            # Eliminar el archivo temporal después de usarlo
            os.remove(qr_path)

            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="turno.pdf"'
            return response
    else:
        form = TurnoForm()

    return render(request, 'authturno/index.html', {'form': form})
