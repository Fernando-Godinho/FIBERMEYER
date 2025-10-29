import os
from .settings import *

# Configurações de produção
DEBUG = True  # Temporariamente True para debug

# Hosts permitidos - permitir tudo temporariamente
ALLOWED_HOSTS = ['*']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Arquivos estáticos
STATIC_URL = '/static/'