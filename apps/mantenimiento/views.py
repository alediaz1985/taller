# apps/mantenimiento/views.py
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from apps.inventario.models import Equipo  # Importa Equipo desde inventario
from .models import Mantenimiento
from .forms import MantenimientoForm, TipoTrabajoForm, ConsultaMantenimientoForm
from django.utils import timezone
from datetime import datetime

from django.db.models import Q


@login_required
def registrar_mantenimiento(request):
    mantenimiento_form = MantenimientoForm(request.POST or None)
    tipo_trabajo_form = TipoTrabajoForm(request.POST or None)

    if request.method == 'POST':
        if 'add_tipo_trabajo' in request.POST and tipo_trabajo_form.is_valid():
            tipo_trabajo_form.save()
            messages.success(request, "Tipo de trabajo añadido exitosamente.")
            return redirect('mantenimiento:registrar_mantenimiento')

        if mantenimiento_form.is_valid():
            mantenimiento = mantenimiento_form.save(commit=False)
            mantenimiento.responsable = request.user  # Asigna el usuario autenticado
            mantenimiento.save()
            messages.success(request, "Mantenimiento registrado exitosamente.")
            return redirect('mantenimiento:registrar_mantenimiento')


    context = {
        'title': 'Registrar Mantenimiento',
        'mantenimiento_form': mantenimiento_form,
        'tipo_trabajo_form': tipo_trabajo_form,
    }
    return render(request, 'mantenimiento/registrar_mantenimiento.html', context)

@login_required
def consulta_mantenimientos(request):
    form = ConsultaMantenimientoForm(request.POST or None)
    mantenimientos = []

    if request.method == 'POST' and form.is_valid():
        fecha_inicio = form.cleaned_data.get('fecha_inicio')
        fecha_fin = form.cleaned_data.get('fecha_fin')
        equipo = form.cleaned_data.get('equipo')
        texto = form.cleaned_data.get('texto_busqueda')
        tipo_busqueda = form.cleaned_data.get('tipo_busqueda')

        mantenimientos = Mantenimiento.objects.all()

        # Filtrar por fechas
        if fecha_inicio:
            mantenimientos = mantenimientos.filter(fecha__gte=fecha_inicio)
        if fecha_fin:
            mantenimientos = mantenimientos.filter(fecha__lte=fecha_fin)

        # Filtrar por texto según el tipo de búsqueda
        if texto and tipo_busqueda:
            if tipo_busqueda == 'nombre':
                mantenimientos = mantenimientos.filter(
                    Q(equipo__marca__icontains=texto) |
                    Q(equipo__modelo__icontains=texto)
                )
            elif tipo_busqueda == 'codigo_interno':
                mantenimientos = mantenimientos.filter(
                    equipo__codigo_interno__icontains=texto
                )
            elif tipo_busqueda == 'numero_serie':
                if "*" in texto:
                    mantenimientos = mantenimientos.filter(
                        equipo__numero_serie__icontains=texto
                    )
                else:
                    mantenimientos = mantenimientos.filter(
                        equipo__numero_serie__iexact=texto
                    )
        else:
            # Si no se ingresó texto pero se seleccionó un equipo puntual
            if equipo:
                mantenimientos = mantenimientos.filter(equipo=equipo)

        # Generar PDF si se solicitó
        if 'generar_pdf' in request.POST:
            return generar_pdf(request, mantenimientos)

    context = {
        'title': 'Consultar Mantenimiento',
        'form': form,
        'mantenimientos': mantenimientos,
    }
    return render(request, 'mantenimiento/consulta_mantenimientos.html', context)


@login_required
def generar_pdf(request, mantenimientos):
    current_date = datetime.now().strftime("%d-%m-%Y %H:%M")
    template = get_template('mantenimiento/reporte_mantenimientos.html')
    
    html = template.render({
        'mantenimientos': mantenimientos,
        'current_date': current_date,
        'nombre_empresa': settings.NOMBRE_EMPRESA,
        'direccion_empresa': settings.DIRECCION_EMPRESA,
        'telefono_empresa': settings.TELEFONO_EMPRESA,
        'email_empresa': settings.EMAIL_EMPRESA,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_mantenimientos.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error al generar el PDF", status=500)
    return response
