from django.shortcuts import render, redirect, get_object_or_404
from .models import Turno
from .forms import TurnoForm
from datetime import time, datetime, timedelta

from django.shortcuts import render, redirect
from .models import Turno
from .forms import TurnoForm
from datetime import date, time, datetime, timedelta

from django.shortcuts import render, redirect, get_object_or_404
from .models import Turno
from .forms import TurnoForm
from datetime import datetime

def reservar_turno(request, fecha, hora, linea):
    if request.method == 'POST':
        form = TurnoForm(request.POST)
        if form.is_valid():
            # Crear y guardar el turno
            turno = form.save(commit=False)
            turno.fecha = fecha
            turno.hora = hora
            turno.linea = linea
            turno.reservado = True
            turno.save()
            return redirect('turnos:cuadrilla_turnos', fecha=fecha)
    else:
        form = TurnoForm()

    return render(request, 'turnos/reservar_turno.html', {'form': form, 'fecha': fecha, 'hora': hora, 'linea': linea})


def generar_horarios(linea):
    horarios = []
    intervalo = 10 if linea == 'livianos' else 15
    hora_actual = time(7, 30)
    while hora_actual < time(12, 0):
        horarios.append(hora_actual)
        hora_actual = (datetime.combine(datetime.today(), hora_actual) + timedelta(minutes=intervalo)).time()

    hora_actual = time(15, 30)
    while hora_actual < time(19, 0):
        horarios.append(hora_actual)
        hora_actual = (datetime.combine(datetime.today(), hora_actual) + timedelta(minutes=intervalo)).time()

    return horarios

def seleccionar_fecha(request):
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        return redirect('turnos:seleccionar_linea', fecha=fecha)
    return render(request, 'turnos/seleccionar_fecha.html')

def seleccionar_linea(request, fecha):
    vehiculos = {
        'livianos': ['gol', 'voyage', 'aveo', 'prisma', 'suran', '206', '207', '208', '307', 'audi_a5'],
        'mixta': ['408', '508', 'ecosport', 'hilux', 'corolla']
    }

    if request.method == 'POST':
        vehiculo = request.POST.get('vehiculo')
        linea = 'livianos' if vehiculo in vehiculos['livianos'] else 'mixta'
        return redirect('turnos:lista_turnos', fecha=fecha, linea=linea)

    return render(request, 'turnos/seleccionar_linea.html', {'fecha': fecha})

def lista_turnos(request, fecha, linea):
    turnos_reservados = Turno.objects.filter(fecha=fecha, linea=linea)
    turnos_disponibles = generar_horarios(linea)

    # Mapear horarios con estados
    turnos_con_estados = []
    for horario in turnos_disponibles:
        estado = 'disponible'
        for turno in turnos_reservados:
            if turno.hora == horario:
                estado = 'reservado' if turno.reservado else 'pendiente'
                break
        turnos_con_estados.append({'hora': horario, 'estado': estado})

    return render(request, 'turnos/lista_turnos.html', {'turnos': turnos_con_estados, 'fecha': fecha, 'linea': linea})


from django.db.models import Count
from django.shortcuts import render
from .models import Turno

def turnos_registrados(request):
    # Agrupar turnos por fecha y contar la cantidad de turnos por día
    turnos_por_dia = Turno.objects.values('fecha').annotate(total=Count('id')).order_by('fecha')

    return render(request, 'turnos/turnos_registrados.html', {'turnos_por_dia': turnos_por_dia})

def detalles_turnos(request, fecha):
    # Obtener todos los turnos registrados para la fecha específica
    turnos = Turno.objects.filter(fecha=fecha).order_by('hora')
    return render(request, 'turnos/detalles_turnos.html', {'fecha': fecha, 'turnos': turnos})




from django.shortcuts import render, redirect
from .models import Turno
from datetime import datetime, time, timedelta

def turnos_por_fecha(request):
    if request.method == 'POST':
        # Obtener la fecha seleccionada del formulario
        fecha = request.POST.get('fecha')
        return redirect('turnos:cuadrilla_turnos', fecha=fecha)

    return render(request, 'turnos/seleccionar_fecha.html')

def cuadrilla_turnos(request, fecha):
    # Generar horarios para cada línea
    horarios_livianos = generar_horarios('livianos')
    horarios_mixta = generar_horarios('mixta')

    # Obtener turnos ya registrados para la fecha
    turnos_registrados = Turno.objects.filter(fecha=fecha)

    # Marcar los estados de los turnos
    turnos_livianos = [{'hora': h, 'estado': obtener_estado(h, 'livianos', turnos_registrados)} for h in horarios_livianos]
    turnos_mixta = [{'hora': h, 'estado': obtener_estado(h, 'mixta', turnos_registrados)} for h in horarios_mixta]

    return render(request, 'turnos/cuadrilla_turnos.html', {
        'fecha': fecha,
        'turnos_livianos': turnos_livianos,
        'turnos_mixta': turnos_mixta
    })

def obtener_estado(hora, linea, turnos_registrados):
    for turno in turnos_registrados:
        if turno.hora == hora and turno.linea == linea:
            return 'reservado' if turno.reservado else 'pendiente'
    return 'disponible'