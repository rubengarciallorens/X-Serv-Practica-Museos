from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from .models import Museo
from .parser import parserXML
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy

# Create your views here.

@csrf_exempt
def auth_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        login(request, user)
        return HttpResponseRedirect("/")

def logout(request):
    logout(request);
    return HttpResponseRedirect("/")

@csrf_exempt
def pos_list(request):
    if request.method =="GET":
        if not request.user.is_authenticated():
            inicio = "<form action='/login' method='post'>"
            inicio += "<label for='username'>Username:</label>"
            inicio += "<input type='text' name='username'"
            inicio += "<label for='password'>Password:</label>"
            inicio += "<input type='password' name='password'>"

            inicio += "<input type='submit' value='LOGIN' />"

        if request.user.is_authenticated():
            inicio = "<p>Bienvenido, "
            inicio += request.user.username
            inicio += "<a href='/logout'> Logout </a></p>"
#                    respuesta += "<form action='/' method='post'>"
#                    respuesta += "<input type= 'hidden' name='opcion' value='1'>"
#                    respuesta += "<input type= 'submit' value='Actualizar'>"
#                    respuesta += "</form>"

    elif request.method == "POST":
        if not request.user.is_authenticated():
            inicio = "<form action='/login' method='post'>"
            inicio += "<label for='username'>Username:</label>"
            inicio += "<input type='text' name='username'"
            inicio += "<label for='password'>Password:</label>"
            inicio += "<input type='password' name='password'>"

            inicio += "<input type='submit' value='LOGIN' />"

        if request.user.is_authenticated():
            inicio = "<p>Bienvenido, "
            inicio += request.user.username
            inicio += "<a href='/logout'> Logout </a></p>"

        if len(Museo.objects.all()) == 0:
            parserXML('./museos/museos.xml')
            return redirect("/")
        respuesta = "<br> Datos actualizados <br>"

    museos = Museo.objects.all()
    c = Context({'inicio':  inicio})
    template = get_template ('home.html')
    respuesta = template.render(c)
    return HttpResponse(respuesta)
