# apps/inventario/views.py
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Equipo, HistorialBaja, TipoBien
from .forms import EquipoForm, BajaForm
from .forms import TipoBienForm
from .forms import EquipoForm
from django.http import JsonResponse

from .permissions import es_administrador  # Asegúrate de tener la función `es_administrador`

from django.core.exceptions import ValidationError


from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


def index(request):
    return render(request, 'inventario/index.html')



def es_administrador(user):
    return user.is_superuser

@login_required
def lista_equipos(request):
    tipo_bien_id = request.GET.get('tipo_bien')
    equipos = Equipo.objects.all()
    
    if tipo_bien_id:
        equipos = equipos.filter(tipo_bien_id=tipo_bien_id)

    tipos_bien = TipoBien.objects.all()

    context = {
        'title': 'Lista de Equipos',
        'equipos': equipos,
        'tipos_bien': tipos_bien,
    }
    return render(request, 'inventario/lista_equipos.html', context)

def generar_pdf_equipos(request):
    tipo_bien_id = request.GET.get('tipo_bien')
    equipos = Equipo.objects.all()

    if tipo_bien_id:
        equipos = equipos.filter(tipo_bien_id=tipo_bien_id)

    template = get_template('inventario/reporte_equipos.html')
    html = template.render({'equipos': equipos})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_equipos.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("Error al generar el PDF", status=500)
    
    return response

@login_required
@user_passes_test(es_administrador)
def registrar_equipo(request):
    if request.method == 'POST':
        form = EquipoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventario:lista_equipos')
    else:
        form = EquipoForm()
    return render(request, 'inventario/registrar_equipo.html', {'form': form})

@login_required
@user_passes_test(es_administrador)
def editar_equipo(request, pk):
    equipo = get_object_or_404(Equipo, pk=pk)
    if request.method == 'POST':
        form = EquipoForm(request.POST, instance=equipo)
        if form.is_valid():
            form.save()
            messages.success(request, "Equipo actualizado exitosamente.")
            return redirect('inventario:lista_equipos')
    else:
        form = EquipoForm(instance=equipo)
    return render(request, 'inventario/editar_equipo.html', {'form': form, 'equipo': equipo})

@login_required
@user_passes_test(es_administrador)
def dar_baja_equipo(request, pk):
    equipo = get_object_or_404(Equipo, pk=pk)
    if request.method == 'POST':
        form = BajaForm(request.POST)
        if form.is_valid():
            baja = form.save(commit=False)
            baja.equipo = equipo
            baja.registrado_por = request.user
            baja.save()
            equipo.activo = False
            equipo.save()
            messages.success(request, "Equipo dado de baja exitosamente.")
            return redirect('inventario:lista_equipos')
    else:
        form = BajaForm()
    return render(request, 'inventario/dar_baja_equipo.html', {'form': form, 'equipo': equipo})

@login_required
def historial_baja_equipo(request, pk):
    equipo = get_object_or_404(Equipo, pk=pk)
    historial = equipo.historial_bajas.all()
    return render(request, 'inventario/historial_baja_equipo.html', {'equipo': equipo, 'historial': historial})


# Decorador para verificar si el usuario es administrador
def admin_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

@admin_required
@login_required
def lista_tipos_bien(request):
    tipos_bien = TipoBien.objects.all()
    return render(request, 'inventario/lista_tipos_bien.html', {'tipos_bien': tipos_bien})


@login_required
@user_passes_test(es_administrador)
def agregar_tipo_bien(request):
    if request.method == 'POST':
        form = TipoBienForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tipo de Bien registrado exitosamente.")
            return redirect('inventario:lista_tipos_bien')
        else:
            # Añadir un mensaje de error si el formulario no es válido
            messages.error(request, "No se pudo registrar el Tipo de Bien. Puede que ya esté registrado el Tipo de Bien o el Prefijo del Código Interno.")
    else:
        form = TipoBienForm()
    return render(request, 'inventario/agregar_tipo_bien.html', {'form': form})




@admin_required
@login_required
def editar_tipo_bien(request, tipo_bien_id):
    tipo_bien = get_object_or_404(TipoBien, id=tipo_bien_id)
    if request.method == 'POST':
        form = TipoBienForm(request.POST, instance=tipo_bien)
        if form.is_valid():
            form.save()
            messages.success(request, "Tipo de Bien actualizado exitosamente.")
            return redirect('inventario:lista_tipos_bien')
    else:
        form = TipoBienForm(instance=tipo_bien)
    return render(request, 'inventario/editar_tipo_bien.html', {'form': form})

@admin_required
@login_required
def eliminar_tipo_bien(request, tipo_bien_id):
    tipo_bien = get_object_or_404(TipoBien, id=tipo_bien_id)
    try:
        tipo_bien.delete()
        messages.success(request, "Tipo de Bien eliminado exitosamente.")
    except ValidationError as e:
        # Muestra un mensaje de error sin generar una excepción
        messages.error(request, str(e))  # Convierte el mensaje de error en texto y lo muestra

    return redirect('inventario:lista_tipos_bien')


def obtener_numero_inventario(request):
    tipo_bien_id = request.GET.get('tipo_bien_id')
    try:
        tipo_bien = TipoBien.objects.get(id=tipo_bien_id)
        ultimo_equipo = Equipo.objects.filter(tipo_bien=tipo_bien).order_by('id').last()
        if ultimo_equipo:
            ultimo_numero = int(ultimo_equipo.codigo_interno.split('-')[1])
            nuevo_numero = ultimo_numero + 1
        else:
            nuevo_numero = 1
        codigo_interno = f"{tipo_bien.prefijo}-{nuevo_numero:03d}"
        return JsonResponse({'codigo_interno': codigo_interno})
    except TipoBien.DoesNotExist:
        return JsonResponse({'error': 'Tipo de bien no encontrado'}, status=404)
    

def generar_etiquetas_equipos(request):
    # Configuración del archivo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="etiquetas_bienes.pdf"'
    
    # Tamaño de la hoja en orientación vertical
    c = canvas.Canvas(response, pagesize=A4)

    # Crear el canvas y definir los metadatos
    c.setTitle("Etiquetas de Bienes")
    c.setSubject("Etiquetas de rotulado para bienes")
    c.setAuthor("Revinor S.R.L. ")
    c.setCreator("Dalis Informática")
    
    # Dimensiones de las etiquetas
    etiqueta_ancho = 65 * mm
    etiqueta_alto = 40 * mm
    margen_izquierdo = 7 * mm
    margen_superior = 7 * mm
    espacio_entre_etiquetas_x = 2 * mm
    espacio_entre_etiquetas_y = 2 * mm

    # Posición inicial para la primera etiqueta
    x = margen_izquierdo
    y = A4[1] - margen_superior - etiqueta_alto

    # Consulta de equipos
    # para imprimir etiqueta de todos los equipos
    # equipos = Equipo.objects.all()

    equipos = Equipo.objects.filter(activo=True)  # Solo equipos activos

    for i, equipo in enumerate(equipos):
        # Crear una nueva página cuando se completan 3 columnas y 7 filas (21 etiquetas por página)
        if i > 0 and i % (3 * 7) == 0:
            c.showPage()
            x = margen_izquierdo
            y = A4[1] - margen_superior - etiqueta_alto

        # Dibujar borde de la etiqueta con esquinas redondeadas
        c.roundRect(x, y, etiqueta_ancho, etiqueta_alto, 5 * mm)

        y_offset = y + etiqueta_alto - 30
        c.setFont("Helvetica-Bold", 14)  # Cambia el tamaño a 10 o el que prefieras
        c.drawString(x + 5, y_offset, f"Código Interno: {equipo.codigo_interno}")
        c.setFont("Helvetica-Bold", 10)
        y_offset -= 25
        c.drawString(x + 5, y_offset, f"Tipo: {equipo.tipo_bien.nombre}")
        y_offset -= 10
        c.drawString(x + 5, y_offset, f"Marca: {equipo.marca}")
        y_offset -= 10
        c.drawString(x + 5, y_offset, f"Modelo: {equipo.modelo}")
        y_offset -= 10
        c.drawString(x + 5, y_offset, f"Número de Serie: {equipo.numero_serie}")
        y_offset -= 10
        c.drawString(x + 5, y_offset, f"Fecha de Compra: {equipo.fecha_compra.strftime('%d-%m-%Y')}")

        # Posiciona la siguiente etiqueta en la fila
        x += etiqueta_ancho + espacio_entre_etiquetas_x

        # Si completamos una fila de 3 etiquetas, saltar a la siguiente fila
        if (i + 1) % 3 == 0:
            x = margen_izquierdo
            y -= etiqueta_alto + espacio_entre_etiquetas_y

    # Guardar y cerrar el PDF
    c.save()
    return response