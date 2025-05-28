# base.py
from decouple import config, Csv
import os
from django.contrib.messages import constants as messages

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.administracion',
    'apps.authturno',
    'apps.discapacidad',
    'apps.excombatiente',
    'apps.mantenimiento',
    'apps.inventario',
    'apps.usuarios',
    'apps.notificaciones',
    'apps.pagos',
    'apps.cedulas',
    'apps.contacto',
    'apps.consultas',
    'apps.soporte',
    'apps.turnos',
    'apps.buscadorpdf',
]

MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'error',
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SESSION_COOKIE_AGE = 1800
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

ROOT_URLCONF = 'taller.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'taller', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'taller.settings.nombre_empresa_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'taller.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_L10N = True
USE_TZ = True

NOMBRE_EMPRESA = config('NOMBRE_EMPRESA', default='Mi Empresa')



STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'taller', 'static'),
    os.path.join(BASE_DIR, 'apps', 'authturno', 'buscadorpdf', 'static', 'images'),
]
STATIC_BASE_PATH = os.path.join(BASE_DIR, 'apps', 'authturno', 'buscadorpdf', 'static', 'images')
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

CEDULAS_DIR = 'C:/CEDULAS'
CEDULAS_URL = '/cedulas_pdf/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = 'index_global'
LOGOUT_REDIRECT_URL = 'index_global'

# Variables sensibles externas
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv)

# Email
CONTACT_EMAIL = config('CONTACT_EMAIL')


from django.conf import settings

# Inyectar NOMBRE_EMPRESA globalmente a todos los templates
def nombre_empresa_context(request):
    return {
        'nombre_empresa': settings.NOMBRE_EMPRESA
    }
