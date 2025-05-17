from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView

@login_required
def index(request):
    context = {'title': 'Inicio'}
    return render(request, 'usuarios/index.html', context)

def registro_usuario(request):
    context = {'title': 'Registro de Usuario'}
    return render(request, 'usuarios/registro.html', context)

def perfil_usuario(request):
    context = {'title': 'Perfil de Usuario'}
    return render(request, 'usuarios/perfil.html', context)

class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'  # Asegúrate de usar la plantilla correcta

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'  # Añadir el título al contexto
        return context

def logout_view(request):
    logout(request)
    return redirect('index_global')  # Redirige a la página principal después de cerrar sesión
