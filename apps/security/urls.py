from   django.conf.urls import patterns,url,include
from django import *
from django.template import *
from SIGIF.apps.security.views import *

urlpatterns= patterns('SIGIF.apps.security.views',
                      url(r'^index$','apps.security.viewsindex_view',name="index"),    url(r'^cerrar/$','django.contrib.auth.views.logout_then_login',name='logout'),
                    url(r'^cerrar/$','django.contrib.auth.views.logout_then_login',name='logout'),

                      )
