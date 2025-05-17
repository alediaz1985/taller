# apps/discapacidad/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Discapacitado, Asistencia
from .forms import ConsultaForm, DiscapacitadoForm, TutorForm, AsistenciaForm
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    discapacitados = Discapacitado.objects.all()
    context = {
        'title': 'Discapacidad',
        'discapacitados': discapacitados
    }
    return render(request, 'discapacidad/index.html', context)

@login_required
def verificar(request):
    if request.method == 'POST':
        dni = request.POST.get('dni', '').strip()
        numero_patente = request.POST.get('numero_patente', '').strip()
        accion = request.POST.get('accion')

        # Validar que al menos uno de los campos esté lleno
        if not dni and not numero_patente:
            messages.error(request, "Debe ingresar al menos un DNI o un Número de Patente para continuar.")
            return redirect('discapacidad:index')

        query = Q()

        # Validar que el DNI sea numérico y tenga exactamente 8 dígitos
        if dni:
            if not dni.isdigit():
                messages.error(request, "El DNI debe ser un número.")
                return redirect('discapacidad:index')
            if len(dni) != 8:
                messages.error(request, "El DNI debe tener exactamente 8 dígitos.")
                return redirect('discapacidad:index')
            query |= Q(dni=dni)

        if numero_patente:
            query |= Q(numero_patente__iexact=numero_patente)

        try:
            discapacitado = Discapacitado.objects.get(query)
            if accion == 'registrar_asistencia':
                # Registrar asistencia si el discapacitado existe
                Asistencia.objects.create(discapacitado=discapacitado, fecha_asistencia=timezone.now())
                messages.success(request, f"Asistencia registrada para {discapacitado.nombre} {discapacitado.apellido}.")
                return redirect('discapacidad:index')
            elif accion == 'consultar':
                # Redirigir a la consulta si el discapacitado existe
                return redirect(f"{reverse('discapacidad:consulta')}?dni={dni}&numero_patente={numero_patente}")

        except Discapacitado.DoesNotExist:
            # Redirigir al formulario de registro si no existe
            messages.info(request, "El discapacitado no está registrado. Por favor, regístralo primero.")
            return redirect(f"{reverse('discapacidad:registrar_nuevo')}?dni={dni}&numero_patente={numero_patente}")

        except Discapacitado.MultipleObjectsReturned:
            messages.error(request, "Se encontraron múltiples registros. Por favor, refine su búsqueda.")
            return redirect('discapacidad:index')

    return redirect('discapacidad:index')

@login_required
def consulta_discapacitado(request):
    dni = request.GET.get('dni')
    numero_patente = request.GET.get('numero_patente')

    # Construir una consulta Q para permitir que uno de los dos campos sea válido
    query = Q()
    if dni:
        query |= Q(dni=dni)
    if numero_patente:
        query |= Q(numero_patente__iexact=numero_patente)

    discapacitados = Discapacitado.objects.filter(query)

    if discapacitados.exists():
        return render(request, 'discapacidad/resultado_consulta.html', {'discapacitados': discapacitados})
    else:
        messages.error(request, "No se encontró ningún discapacitado con los datos proporcionados.")
        return redirect('discapacidad:index')


@login_required
def registrar_nuevo(request):
    dni = request.GET.get('dni', '')
    numero_patente = request.GET.get('numero_patente', '')

    if request.method == 'POST':
        discapacitado_form = DiscapacitadoForm(request.POST)
        tutor_form = TutorForm(request.POST) if 'es_menor' in request.POST else None

        if discapacitado_form.is_valid():
            discapacitado = discapacitado_form.save()
            Asistencia.objects.create(discapacitado=discapacitado, fecha_asistencia=timezone.now())

            if tutor_form and tutor_form.is_valid():
                tutor = tutor_form.save(commit=False)
                tutor.discapacitado = discapacitado
                tutor.save()
            elif tutor_form and not tutor_form.is_valid():
                messages.error(request, "Por favor, corrija los errores en el formulario del tutor.")
                return render(request, 'discapacidad/registrar_nuevo.html', {
                    'discapacitado_form': discapacitado_form,
                    'tutor_form': tutor_form,
                })

            messages.success(request, "Discapacitado registrado y asistencia registrada.")
            return redirect('discapacidad:index')

        else:
            messages.error(request, "Por favor, corrija los errores en el formulario del discapacitado.")

    else:
        discapacitado_form = DiscapacitadoForm(initial={'dni': dni, 'numero_patente': numero_patente})
        tutor_form = TutorForm() if 'es_menor' in request.GET else None

    return render(request, 'discapacidad/registrar_nuevo.html', {
        'discapacitado_form': discapacitado_form,
        'tutor_form': tutor_form,
    })

@login_required
def registrar_asistencia(request):
    if request.method == 'POST':
        form = AsistenciaForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data['dni']
            numero_patente = form.cleaned_data['numero_patente']

            # Busca el discapacitado en la base de datos
            discapacitado = Discapacitado.objects.filter(Q(dni=dni) | Q(numero_patente__iexact=numero_patente)).first()

            if discapacitado:
                # Registra la asistencia
                Asistencia.objects.create(
                    discapacitado=discapacitado,
                    fecha_asistencia=timezone.now()
                )
                # Actualiza el número de patente si ha cambiado
                if discapacitado.numero_patente != numero_patente:
                    discapacitado.numero_patente = numero_patente
                    discapacitado.save()

                messages.success(request, f"Asistencia registrada para {discapacitado.nombre} {discapacitado.apellido}.")
                return redirect('discapacidad:index')
            else:
                # Redirige al formulario de registro de discapacitado
                return redirect(f"{reverse('discapacidad:registrar_nuevo')}?dni={dni}&numero_patente={numero_patente}")
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")

    else:
        form = AsistenciaForm()

    return render(request, 'discapacidad/registrar_asistencia.html', {
        'form': form,
    })

@login_required
def registrar_visita(request, dni):
    discapacitado = get_object_or_404(Discapacitado, dni=dni)
    tutor = get_object_or_404(tutor, dni=dni)
    Asistencia.objects.create(discapacitado=discapacitado, fecha_asistencia=timezone.now())
    messages.success(request, f'Visita registrada para {discapacitado.dni} {discapacitado.nombre} {discapacitado.apellido} {tutor}.')
    return HttpResponseRedirect(reverse('discapacidad:consulta'))