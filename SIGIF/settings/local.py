import os
from .base import *

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}



STATICFILES_DIRS = [BASE_DIR.child('static')]
TEMPLATE_DIRS = [BASE_DIR.child('templates')]

STATIC_URL = '/static/'
