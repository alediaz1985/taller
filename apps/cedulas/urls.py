from django.urls import path
from .views import generar_pdf_cedula, listar_cedulas

app_name = 'cedulas'

urlpatterns = [
    path('generar/', generar_pdf_cedula, name='generar_pdf'),
    path('listar/', listar_cedulas, name='listar_cedulas'),  # ✅ nueva URL
]
