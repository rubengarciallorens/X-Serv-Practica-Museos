from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from .models import Museo
from .parser import parserXML
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.contrib.auth.models import User

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
def register(request):
    username = request.POST['user']
    email = request.POST['email']
    password = request.POST['password']
    user = User.objects.create_user(username, email, password)
    user.save()
    return HttpResponseRedirect("/")

@csrf_exempt
def museo_pers(request, id):
    if not request.user.is_authenticated():
        inicio = "<form action='/login' method='post'>"
        inicio += "<label for='username'>Username:</label>"
        inicio += "<input type='text' name='username'"
        inicio += "<label for='password'>Password:</label>"
        inicio += "<input type='password' name='password'>"

        inicio += "<input type='submit' value='LOGIN' />"
        inicio += "</form>"

        registro = "<form action='/register/' method='post'>"
        registro += "User: <input type= 'text' name='user'>"
        registro += "Email: <input type= 'text' name='email'>"
        registro += "Password: <input type= 'password' name='password'>"
        registro += "<input type= 'submit' value='enviar'>"
        registro += "</form>"

    if request.user.is_authenticated():
        inicio = "<p>Bienvenido,  "
        inicio += request.user.username
        inicio += "<a href='/logout'> Logout </a></p>"
        registro = "<p> Se ha identificado usted como: "
        registro += "<h2>" + request.user.username + "</h2>"
        registro +="." + "<br> Esperamos que su visita a la página sea satisfactoria"
    
    museo=Museo.objects.get(identidad=id)    
    content_title = str(museo.nombre)
    c = Context({'inicio': inicio, 'registro': registro, 'content_title': content_title})
    template = get_template ('museo_pers.html')
    respuesta = template.render(c)
    return HttpResponse(respuesta)

@csrf_exempt
def allmuseums(request):
    if not request.user.is_authenticated():
        inicio = "<form action='/login' method='post'>"
        inicio += "<label for='username'>Username:</label>"
        inicio += "<input type='text' name='username'"
        inicio += "<label for='password'>Password:</label>"
        inicio += "<input type='password' name='password'>"

        inicio += "<input type='submit' value='LOGIN' />"
        inicio += "</form>"

        registro = "<form action='/register/' method='post'>"
        registro += "User: <input type= 'text' name='user'>"
        registro += "Email: <input type= 'text' name='email'>"
        registro += "Password: <input type= 'password' name='password'>"
        registro += "<input type= 'submit' value='enviar'>"
        registro += "</form>"

    if request.user.is_authenticated():
        inicio = "<p>Bienvenido,  "
        inicio += request.user.username
        inicio += "<a href='/logout'> Logout </a></p>"

        registro = "<p> Se ha identificado usted como: "
        registro += "<h2>" + request.user.username + "</h2>"
        registro +="." + "<br> Esperamos que su visita a la página sea satisfactoria"
    
    if request.method=="GET":
        if len(Museo.objects.all())==0:
            content_title ="Aún no hay museos cargados"
            content = "<form action='/museos/' method='post'>"
            content += "<button type='submit'>CARGAR</button>"
            content += "</form>"
        else: 
            content_title="Todos los museos comunidad"
            museos = Museo.objects.all ()
            content = ""
            for museo in museos:
                content += "<br><a href=" + museo.url + ">"
                content += museo.nombre + "</a><br>"
                museoid = str(museo.identidad)
                if request.user.is_authenticated():
                    content += "<br><a href='all/"+ museoid +"'> Página propia </a></p><br>"
    
    elif request.method=="POST":
        if len(Museo.objects.all())==0:
            parserXML('./museos/museos.xml')
        content_title ="Museos cargados"
        museos = Museo.objects.all ()
        content = ""
        for museo in museos:
            content += "<br><a href=" + museo.url + ">"
            content += museo.nombre + "  ""</a><br>"
            museoid = str(museo.identidad)
            if request.user.is_authenticated():
                content += "<br><a href='all/"+ museoid +"'> Página propia </a></p><br>"

    c = Context({'inicio': inicio, 'registro': registro, 'content_title': content_title, 'content': content})
    template = get_template ('museos.html')
    respuesta = template.render(c)
    return HttpResponse(respuesta)

@csrf_exempt
def main(request):
    if request.method =="GET":
        if not request.user.is_authenticated():
            inicio = "<form action='/login' method='post'>"
            inicio += "<label for='username'>Username:</label>"
            inicio += "<input type='text' name='username'"
            inicio += "<label for='password'>Password:</label>"
            inicio += "<input type='password' name='password'>"

            inicio += "<input type='submit' value='LOGIN' />"
            inicio += "</form>"

#            registro = "<form action='/register' method='post'>"
            registro = "<form action='/register/' method='post'>"
            registro += "User: <input type= 'text' name='user'>"
            registro += "Email: <input type= 'text' name='email'>"
            registro += "Password: <input type= 'password' name='password'>"
            registro += "<input type= 'submit' value='enviar'>"
            registro += "</form>"
#            registro += "<label for='username'>Usuario:</label>"
#            registro += "<input type='text' name='user'"
#            registro += "<label for='email'>Email:</label>"
#            registro += "<input type='text' name='email'"
#            registro += "<label for='password'>Contraseña:</label>"
#            registro += "<input type='password' name='password'>"

#            registro += "<input type='submit' value='REGISTRAR' />"


        if request.user.is_authenticated():
            inicio = "<p>Bienvenido,  "
            inicio += request.user.username
            inicio += "<a href='/logout'> Logout </a></p>"

            registro = "<p> Se ha identificado usted como: "
            registro += "<h2>" + request.user.username + "</h2>"
            registro +="." + "<br> Esperamos que su visita a la página sea satisfactoria"
#                    respuesta += "<form action='/' method='post'>"
#                    respuesta += "<input type= 'hidden' name='opcion' value='1'>"
#                    respuesta += "<input type= 'submit' value='Actualizar'>"
#                    respuesta += "</form>"

    elif request.method == "POST":
#        if not request.user.is_authenticated():
#            inicio = "<form action='/login' method='post'>"
#            inicio += "<label for='username'>Username:</label>"
#            inicio += "<input type='text' name='username'"
#            inicio += "<label for='password'>Password:</label>"
#            inicio += "<input type='password' name='password'>"

#            inicio += "<input type='submit' value='LOGIN' />"

#        if request.user.is_authenticated():
#            inicio = "<p>Bienvenido, "
#            inicio += request.user.username
#            inicio += "<a href='/logout'> Logout </a></p>"

        if len(Museo.objects.all()) == 0:
            parserXML('./museos/museos.xml')
            return redirect("/")
        respuesta = "<br> Datos actualizados <br>"

    content_title="5 museos más comentados"
    c = Context({'inicio':  inicio, 'registro': registro, 'content_title':content_title})
    template = get_template ('home.html')
    respuesta = template.render(c)
    return HttpResponse(respuesta)
