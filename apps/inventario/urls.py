from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('', views.index, name='index'),
    path('lista/', views.lista_equipos, name='lista_equipos'),
    path('tipos_bien/', views.lista_tipos_bien, name='lista_tipos_bien'),
    path('tipos_bien/agregar/', views.agregar_tipo_bien, name='agregar_tipo_bien'),
    path('tipos_bien/<int:tipo_bien_id>/editar/', views.editar_tipo_bien, name='editar_tipo_bien'),
    path('tipos_bien/<int:tipo_bien_id>/eliminar/', views.eliminar_tipo_bien, name='eliminar_tipo_bien'),
    path('registrar/', views.registrar_equipo, name='registrar_equipo'),
    path('<int:pk>/editar/', views.editar_equipo, name='editar_equipo'),
    path('<int:pk>/baja/', views.dar_baja_equipo, name='dar_baja_equipo'),
    path('<int:pk>/historial/', views.historial_baja_equipo, name='historial_baja_equipo'),
    path('obtener_numero_inventario/', views.obtener_numero_inventario, name='obtener_numero_inventario'),
    path('pdf/', views.generar_pdf_equipos, name='generar_pdf_equipos'),
    path('etiquetas/pdf/', views.generar_etiquetas_equipos, name='generar_etiquetas_equipos'),
]