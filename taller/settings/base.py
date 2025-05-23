import os
from django.contrib.messages import constants as messages

# BASE_DIR apunta al directorio raíz del proyecto.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Application definition
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

# Tiempo de vida de la sesión en segundos
SESSION_COOKIE_AGE = 1800  # 30 minutos

# Cerrar sesión al cerrar el navegador
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Usa sesiones basadas en la base de datos
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

ROOT_URLCONF = 'taller.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'taller', 'templates')],  # Ruta a las plantillas globales
        'APP_DIRS': True,  # Busca automáticamente plantillas en cada aplicación
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'taller.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'es-ar'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'taller', 'static'),
    os.path.join(BASE_DIR, 'apps', 'authturno', 'buscadorpdf', 'static', 'images'),
]
STATIC_BASE_PATH = os.path.join(BASE_DIR, 'apps', 'authturno', 'buscadorpdf', 'static', 'images')

CEDULAS_DIR = 'C:/CEDULAS'
CEDULAS_URL = '/cedulas_pdf/'  # Ruta pública para acceder desde el navegador

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'index_global'
LOGOUT_REDIRECT_URL = 'index_global'


# Correo de contacto que recibiría los mensajes
CONTACT_EMAIL = 'formulariodecorreosp@gmail.com'

