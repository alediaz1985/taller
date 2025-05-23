from django.urls import path
from . import views

app_name = 'buscadorpdf'

urlpatterns = [
    path('buscar/', views.buscar_pdf, name='buscar_pdf'),
    path('exportar/', views.exportar_resultados_pdf, name='exportar_pdf'),
    path('abrir/', views.abrir_archivo_pdf, name='abrir_pdf'),
    path('generar_pdf_contenido/', views.generar_pdf_contenido, name='generar_pdf_contenido'),
]

