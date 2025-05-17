# apps/usuarios/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView, logout_view, index, registro_usuario, perfil_usuario

app_name = 'usuarios'

urlpatterns = [
    path('', views.index, name='index'),
    path('registro/', views.registro_usuario, name='registro_usuario'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    
    # Vista para el inicio de sesión

    #path('accounts/login/', CustomLoginView.as_view(), name='login'),
    
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    
    
    # Vista para el cierre de sesión
    # No necesitas un template para logout ya que simplemente redirige a otra página

    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('accounts/logout/', logout_view, name='logout'),
]

