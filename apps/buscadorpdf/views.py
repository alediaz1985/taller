import os
#import datetime
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from .forms import RutaBusquedaForm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.contrib.auth.decorators import login_required

def detectar_unidades_validas():
    disponibles = []
    for letra in 'CDEFGHIJKLMNOPQRSTUVWXYZ':
        ruta_ensayos = f"{letra}:\\ensayos"
        ruta_raiz = f"{letra}:\\"

        if os.path.exists(ruta_ensayos):
            disponibles.append(ruta_ensayos)
        elif os.path.exists(ruta_raiz):  # unidad montada (red o externa)
            disponibles.append(ruta_raiz)

    return disponibles


def buscar_archivos_pdf(ruta, nombre, fecha_desde=None, fecha_hasta=None):
    resultados = []
    for root, _, files in os.walk(ruta):
        for file in files:
            if not file.lower().endswith(".pdf"):
                continue
            if nombre and nombre.lower() not in file.lower():
                continue

            full_path = os.path.join(root, file)
            timestamp = os.path.getmtime(full_path)
            fecha = datetime.fromtimestamp(os.path.getmtime(full_path))

            if fecha_desde and fecha.date() < fecha_desde:
                continue
            if fecha_hasta and fecha.date() > fecha_hasta:
                continue

            resultados.append({
                'nombre': file,
                'ruta': full_path,
                'fecha': fecha,
            })
    return resultados

@login_required
def buscar_pdf(request):
    resultados = []
    error = ""
    unidades = detectar_unidades_validas()
    form = RutaBusquedaForm(request.GET or None)

    if form.is_valid():
        ruta = form.cleaned_data.get('directorio_busqueda')
        nombre = form.cleaned_data.get('nombre_archivo')
        fecha_desde = form.cleaned_data.get('fecha_desde')
        fecha_hasta = form.cleaned_data.get('fecha_hasta')

        # 🔍 DEPURACIÓN
        print("🛠️ Ruta recibida:", ruta)
        print("🛠️ Normalizada:", os.path.normpath(ruta))
        print("🛠️ Existe:", os.path.exists(ruta))

        if not os.path.exists(ruta):
            error = f"La ruta ingresada no existe: {ruta}"
        else:
            resultados = buscar_archivos_pdf(ruta, nombre, fecha_desde, fecha_hasta)
            resultados = sorted(resultados, key=lambda x: x['fecha'], reverse=True)
            request.session['resultados_encontrados'] = [r['ruta'] for r in resultados]

            if not resultados:
                if nombre:
                    error = f"🔍 No se encontraron resultados con la palabra ingresada: “<strong>{nombre}</strong>”."
                else:
                    error = "🔍 No se encontraron archivos que coincidan con los criterios de búsqueda."


    return render(request, 'buscadorpdf/search.html', {
        'form': form,
        'resultados': resultados,
        'error': error,
        'opciones': unidades,
    })

@login_required
def exportar_resultados_pdf(request):
    ruta = request.GET.get('directorio_busqueda', '').strip()
    nombre = request.GET.get('nombre_archivo', '').strip()
    resultados = buscar_archivos_pdf(ruta, nombre)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resultados_busqueda.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    y = height - 40
    p.setFont("Helvetica", 12)
    p.drawString(40, y, f"Resultados de búsqueda en: {ruta}")
    y -= 30

    for r in resultados:
        if y < 100:
            p.showPage()
            y = height - 40
        p.drawString(40, y, f"{r['fecha'].strftime('%d-%m-%Y %H:%M')} - {r['nombre']}")
        y -= 15
        p.drawString(50, y, f"{r['ruta']}")
        y -= 25

    p.save()
    return response

@login_required
def abrir_archivo_pdf(request):
    ruta = request.GET.get('ruta', '').strip()
    if not ruta or not os.path.exists(ruta):
        return HttpResponse("Archivo no encontrado", status=404)
    return FileResponse(open(ruta, 'rb'), content_type='application/pdf')


#------------------------------------------------------------------------------
#Sirve para generar un pdf con la informacion encontrada
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import letter
from django.http import HttpResponse
from datetime import datetime
from .utils import extraer_texto

from pdf2image import convert_from_path
from io import BytesIO
from reportlab.platypus import Image
from reportlab.lib.units import inch


@login_required
def generar_pdf_contenido(request):
    rutas = request.session.get('resultados_encontrados', [])
    if not rutas:
        return HttpResponse("Error: No hay archivos para generar el PDF")

    # Preparar los datos
    resultados = []
    for ruta in rutas:
        texto = extraer_texto(ruta)
        resultados.append({
            'nombre_archivo': ruta,
            'texto': texto.strip() or "⚠️ No se pudo extraer texto del archivo."
        })

    # Configurar respuesta PDF
    fecha_hora_actual = datetime.now().strftime("%Y-%m-%d-%H%M")
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_texto_{fecha_hora_actual}.pdf"'

    # Crear documento
    doc = SimpleDocTemplate(response, pagesize=letter, title=f"Búsqueda Revinor - {fecha_hora_actual}")
    doc.author = "Revinor S.R.L."

    # Estilos
    style_normal = ParagraphStyle(name='Normal', fontName='Helvetica', fontSize=10)
    style_body = ParagraphStyle(name='Body', fontName='Helvetica', fontSize=10)
    style_code = ParagraphStyle(name='Code', fontName='Courier-Bold', fontSize=10, leading=14)
    style_title = ParagraphStyle(name='Title', fontName='Helvetica-Bold', fontSize=18, alignment=1)

    # Contenido del documento
    content = []

    f = "_" * 80
    titulo = "Revinor S.R.L."
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    content.append(Paragraph(titulo, style_title))
    content.append(Paragraph(f, style_body))
    content.append(Spacer(1, 12))
    content.append(Paragraph(f"Fecha y hora de búsqueda: {fecha_hora}", style_body))
    content.append(Paragraph(f, style_body))
    content.append(Spacer(1, 12))

    for resultado in resultados:
        ruta_archivo = resultado.get('nombre_archivo', '')
        texto_extraido = resultado.get('texto', '')
        content.append(Paragraph(f"Ruta del archivo: {ruta_archivo}", style_body))
        content.append(Spacer(1, 6))
        content.append(Preformatted(texto_extraido, style_code))
        content.append(Spacer(1, 12))
        content.append(Paragraph(f, style_body))

    doc.build(content)
    return response
