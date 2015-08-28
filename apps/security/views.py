from django.shortcuts import render,HttpResponseRedirect, render_to_response, RequestContext
from models import *
from django.contrib.auth import *

def index_view(request):
    return render_to_response('index.html',context=RequestContext(request))

def login_view(request):
    return  render_to_response('login.html',context=RequestContext(request))



