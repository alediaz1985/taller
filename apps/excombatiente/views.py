# apps/excombatiente/views.py
from django.shortcuts import render
from .models import ExCombatiente
from .forms import ConsultaDNIForm
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    form = ConsultaDNIForm()
    resultado = None

    if request.method == 'POST':
        form = ConsultaDNIForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data['dni']
            try:
                excombatiente = ExCombatiente.objects.get(dni=dni)
                resultado = excombatiente
            except ExCombatiente.DoesNotExist:
                resultado = "No se encontró ningún excombatiente con ese DNI."

    context = {
        'title': 'Consulta de Excombatientes',
        'form': form,
        'resultado': resultado
    }
    return render(request, 'excombatiente/index.html', context)
