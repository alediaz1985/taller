from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'tu-clave-secreta-en-produccion'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['tu_dominio.com', 'www.tu_dominio.com']

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nombre_de_tu_base_de_datos',
        'USER': 'usuario',
        'PASSWORD': 'contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Solo enviar cookies a través de HTTPS en producción
SESSION_COOKIE_SECURE = True

# Configuración de archivos estáticos para producción
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'formulariodecorreosp@gmail.com'
EMAIL_HOST_PASSWORD = 'Yupi2000'
