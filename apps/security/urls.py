from   django.conf.urls import patterns,url,include
from django import *
from django.template import *
from SIGIF.apps.security.views import *

urlpatterns= patterns('SIGIF.apps.security.views',
                      url(r'^index$','index_view',name="index"),
                      )