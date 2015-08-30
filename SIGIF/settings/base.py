from unipath import Path
from django.http import HttpResponse

BASE_DIR = Path(__file__).ancestor(3)

SECRET_KEY = 'w#rr_9b1n5z0!6v3q%gak4-yf*sk5huvlg8+5ys0k(+1=hb^r='

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (

)

LOCAL_APPS = (
    'apps.Clientes',
    'apps.Factura',
    'apps.Pedidos',
    'apps.Productos',
    'apps.Proveedores',
    'apps.security',
    'apps.Usuarios',
    'bootstrap3'
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

from django.core.urlresolvers import reverse_lazy
LOGIN_URL= reverse_lazy('login')
LOGIN_REDIRECT_URL= reverse_lazy('index')
LOGOUT_URL=reverse_lazy('logout')

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'SIGIF.urls'

WSGI_APPLICATION = 'SIGIF.wsgi.application'

LANGUAGE_CODE = 'es-ES'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.template.context_processors.debug',
    'django.template.context_processors.request',
    'django.template.context_processors.media',
    'django.template.context_processors.static',
    'django.template.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
)



AUTH_USER_MODEL = 'security.Usuario'
