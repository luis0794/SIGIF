from django.shortcuts import render,HttpResponseRedirect, render_to_response, RequestContext
from models import *
from django.contrib.auth import *
from django.contrib.auth.decorators import login_required


@login_required(login_url='/')
def index_view(request):
    return render_to_response('index.html',context=RequestContext(request))
@login_required(login_url='/')
def login_view(request):
    return  render_to_response('login.html',context=RequestContext(request))



