# apps/cedulas/views.py
import os
from pathlib import Path
from django.shortcuts import render
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from datetime import datetime
from io import BytesIO
from PIL import Image
from .forms import CedulaForm
import locale

from django.conf import settings
from .models import Cedula
from django.utils.timezone import make_aware
from datetime import datetime, timedelta

from PIL import Image

def recortar(imagen, crop_data):
    x, y, w, h = map(int, crop_data.split(","))
    imagen_pil = Image.open(imagen)
    return imagen_pil.crop((x, y, x + w, y + h))


@login_required
def generar_pdf_cedula(request):
    if request.method == 'POST':
        dominio = request.POST.get('dominio')
        frente_file = request.FILES.get('frente')
        dorso_file = request.FILES.get('dorso')

        if not (dominio and frente_file and dorso_file):
            return render(request, 'cedulas/subir_imagenes.html', {'error': 'Faltan datos'})

        frente_crop = request.POST.get("frente_crop")
        dorso_crop = request.POST.get("dorso_crop")

        frente_img = recortar(frente_file, frente_crop) if frente_crop else Image.open(frente_file)
        dorso_img = recortar(dorso_file, dorso_crop) if dorso_crop else Image.open(dorso_file)


        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)

        # Título y metadatos del PDF
        p.setTitle(f"Cédula - {dominio.upper()}")
        p.setAuthor(f"Sistema Revinor - {request.user.get_full_name() or request.user.username}")
        p.setSubject(f"Cédula del dominio {dominio.upper()}")
        p.setKeywords("cédula, dominio, pdf, Revinor, frente, dorso")
        p.setCreator("DALIS - Informática")


        ancho_mm = 85
        alto_mm = 56
        x_frente = 20 * mm
        x_dorso = (20 + 90) * mm
        y_base = 220 * mm

        fecha = datetime.now().strftime('%d/%m/%Y')
        encabezado = f"Dominio: {dominio.upper()}    Fecha: {fecha}"
        page_width, _ = A4
        p.setFont("Helvetica-Bold", 14)
        text_width = p.stringWidth(encabezado, "Helvetica-Bold", 14)
        p.drawString((page_width - text_width) / 2, y_base + 65 * mm, encabezado)


        def dibujar(imagen, x, y):
            max_width = ancho_mm * mm
            max_height = alto_mm * mm

            # Convertir imagen a alta resolución para impresión (300dpi virtuales)
            temp_io = BytesIO()
            imagen.save(temp_io, format='PNG', dpi=(300, 300))  # Forzamos DPI alto
            temp_io.seek(0)

            img_reader = ImageReader(temp_io)
            iw, ih = imagen.size
            aspect = iw / ih
            target_aspect = max_width / max_height

            if aspect > target_aspect:
                new_width = max_width
                new_height = max_width / aspect
            else:
                new_height = max_height
                new_width = max_height * aspect

            p.drawImage(img_reader,
                        x + (max_width - new_width) / 2,
                        y + (max_height - new_height) / 2,
                        width=new_width,
                        height=new_height,
                        preserveAspectRatio=True)
            
        dibujar(frente_img, x_frente, y_base)
        dibujar(dorso_img, x_dorso, y_base)

        observaciones = request.POST.get('observaciones', '').strip()
        if observaciones:
            p.setFont("Helvetica", 12)
            p.setFillColorRGB(0.2, 0.2, 0.2)  # Gris oscuro
            texto_obs = f"Observaciones: {observaciones}"
            p.drawString(20 * mm, y_base + -5 * mm, texto_obs)

        p.showPage()
        p.save()
        buffer.seek(0)

        # Guardar en disco como antes
        hoy = datetime.now()
        año = str(hoy.year)

        # Configurar locale en español para obtener el nombre del mes en español
        try:
            locale.setlocale(locale.LC_TIME, 'Spanish_Argentina')  # Para Windows
        except locale.Error:
            try:
                locale.setlocale(locale.LC_TIME, 'es_AR.utf8')  # Para Linux
            except locale.Error:
                locale.setlocale(locale.LC_TIME, '')  # Valor por defecto del sistema

        MES = hoy.strftime("%m %B").title()  # Ejemplo: "05 Mayo"

        dia = f"{hoy.day:02}"

        carpeta = Path(f"C:/CEDULAS/{año}/{MES}/{dia}")
        carpeta.mkdir(parents=True, exist_ok=True)

        ruta_pdf = carpeta / f"{dominio.upper()}_cedula.pdf"
        with open(ruta_pdf, 'wb') as f:
            f.write(buffer.getbuffer())

        # Guardar solo la ruta relativa a C:/CEDULAS para que se pueda usar por URL
        ruta_relativa = ruta_pdf.relative_to(Path(settings.CEDULAS_DIR))

        observaciones = request.POST.get('observaciones', '')

        Cedula.objects.create(
            dominio=dominio.upper(),
            ruta_pdf=str(ruta_relativa).replace('\\', '/'),  # ejemplo: 2025/Mayo/17/ABC123_cedula.pdf
            usuario=request.user,
            observaciones=observaciones
        )


        return FileResponse(buffer, as_attachment=True, filename=ruta_pdf.name)

    return render(request, 'cedulas/subir_imagenes.html')



@login_required
def listar_cedulas(request):
    cedulas = Cedula.objects.all()

    # Filtros GET
    dominio = request.GET.get('dominio')
    desde = request.GET.get('desde')
    hasta = request.GET.get('hasta')

    if dominio:
        cedulas = cedulas.filter(dominio__icontains=dominio)

    if desde:
        try:
            desde_dt = make_aware(datetime.strptime(desde, '%Y-%m-%d'))
            cedulas = cedulas.filter(fecha_subida__gte=desde_dt)
        except ValueError:
            pass  # fecha inválida, ignoramos filtro

    if hasta:
        try:
            hasta_dt = make_aware(datetime.strptime(hasta, '%Y-%m-%d') + timedelta(days=1))
            cedulas = cedulas.filter(fecha_subida__lt=hasta_dt)
        except ValueError:
            pass  # fecha inválida, ignoramos filtro

    cedulas = cedulas.order_by('-fecha_subida')

    # Verificar existencia del archivo
    for c in cedulas:
        try:
            if c.ruta_pdf:
                ruta_absoluta = Path(settings.CEDULAS_DIR) / c.ruta_pdf
                c.archivo_existe = ruta_absoluta.exists()
            else:
                c.archivo_existe = False
        except Exception:
            c.archivo_existe = False

    return render(request, 'cedulas/listar_cedulas.html', {'cedulas': cedulas})
