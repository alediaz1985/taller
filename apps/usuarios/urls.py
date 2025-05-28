from django.urls import path
from .views import CustomLoginView, logout_view, index, registro_usuario, perfil_usuario

app_name = 'usuarios'

urlpatterns = [
    path('', index, name='index'),
    path('registro/', registro_usuario, name='registro_usuario'),
    path('perfil/', perfil_usuario, name='perfil_usuario'),
    
    # ✅ Usar tu vista personalizada
    path('login/', CustomLoginView.as_view(), name='login'),

    # Logout
    path('accounts/logout/', logout_view, name='logout'),
]
