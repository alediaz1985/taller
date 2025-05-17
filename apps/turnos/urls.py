from django.urls import path
from . import views

app_name = 'turnos'

urlpatterns = [
    path('', views.turnos_por_fecha, name='turnos_por_fecha'),
    #path('', views.seleccionar_fecha, name='seleccionar_fecha'),
    path('linea/<str:fecha>/', views.seleccionar_linea, name='seleccionar_linea'),
    path('turnos/<str:fecha>/<str:linea>/', views.lista_turnos, name='lista_turnos'),
    path('registrados/', views.turnos_registrados, name='turnos_registrados'),
    path('detalles/<str:fecha>/', views.detalles_turnos, name='detalles_turnos'),
    path('cuadrilla/<str:fecha>/', views.cuadrilla_turnos, name='cuadrilla_turnos'),
    path('reservar/<str:fecha>/<str:hora>/<str:linea>/', views.reservar_turno, name='reservar_turno'),
]
