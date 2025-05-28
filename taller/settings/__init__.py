import os

env = os.getenv('DJANGO_ENV', 'local').lower()

if env == 'production':
    print("✔ Configuración: PRODUCTION")
    from .production import *
else:
    print("✔ Configuración: LOCAL")
    from .local import *
