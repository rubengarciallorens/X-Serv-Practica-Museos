from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from .models import Museo, Comentario, Seleccion
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
def personal (request, propietario):
    if not request.user.is_authenticated():
        inicio = "<form action='/login' method='post'>"
        inicio += "<label for='username'>Username:</label>"
        inicio += "<input type='text' name='username'"
        inicio += "<label for='password'>Password:</label>"
        inicio += "<input type='password' name='password'>"
        inicio += "<input type='submit' value='LOGIN' />"
        inicio += "</form>"

    if request.user.is_authenticated():
        inicio = "<p>Bienvenido,  "
        inicio += request.user.username
        inicio += "<a href='/logout'> Logout </a></p>"

    if request.method == "GET":
        content="No tienes museos añadidos aún a tu lista"
    elif request.method =="POST":
        content = "No tienes museos añadidos aún a tu lista"
    content_title="Página de " + str(request.user.username)
    c = Context({'inicio': inicio, 'content_title': content_title, 'content': content})
    template = get_template ('museo_pers.html')
    respuesta = template.render(c)
    return HttpResponse(respuesta)

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

    if request.method=="POST":
        texto = request.POST['texto']
        comentario = Comentario (museo = museo , texto= texto)
        comentario.save()
        museo.num_comentarios=museo.num_comentarios + 1
        museo.save()

    content = "<br><li>Descripción entidad:</li><p>" + str(museo.descripcion_entidad) + "</p><br>"
    content += "<br><li>Transporte:</li><p>" + str(museo.transporte) + "</p><br>"
    content += "<br><li>Equipamiento:</li><p>" + str(museo.equipamiento) + "</p><br>"
    content += "<br><li>Descripción:</li><p>" + str(museo.descripcion) + "</p><br>"
    content += "<br><li>Horario:</li><p>" + str(museo.horario) + "</p><br>"
    content += "<br><li>URL del sitio:</li> <a href ='" + museo.url + "'>" + str(museo.url) + "</a><br>"
    content += "<br><li>Localización:</li><p>" + str(museo.localizacion) + "</p><br>"
    content += "<br><li>Contacto:</li>"
    content += "<p>Telefono: " + str(museo.telefono) + "</p>"
    content += "<p>Fax: " + str(museo.fax) + "</p>"
    content += "<p>Email: " + str(museo.email) + "</p>"
    opiniones = Comentario.objects.filter(museo=museo)
    content += "<br><li>Comentarios:</li>"
    num=1
    for opinion in opiniones:
        content += "<p>"+ str(num) + " - " + opinion.texto + "</p>"
        num=num+1

    if request.user.is_authenticated():
        content += "<br><li> Añadir comentario: </li></br>"
        content += "<form action='/museos/" + str(id) + "' method=POST>"
        content += "<input type= 'text' name='texto'>"
        content += "<input type= 'hidden' name='opcion' value='1'>"
        content += "<input type= 'submit' value='enviar'>"
        content += "</form>"
    if not request.user.is_authenticated():
        content += "<br><li>Podrá añadir comentarios cuando se registre en la página y se identifique. </li>"
    c = Context({'inicio': inicio, 'registro': registro, 'content_title': content_title, 'content': content})
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
                museoid = str(museo.identidad)
                content += "<br><a href=museos/" + museoid + ">"
                content += museo.nombre + "</a><br>"
                content += "<br><li>URL del sitio: </li> <a href='" + museo.url +"'> " + museo.url + "</a></br>"
                if request.user.is_authenticated():
                    content += "<form action='/museos' method=POST>"
                    content += "<input type= 'text' name='texto'>
                    content += "<input type= 'hidden' name='opcion' value='1'>"
                    content += "<input type= 'submit' value='enviar'>"
                    content += "</form>
                content += "<br> ---------------------------------------------------------------------------------------------------------------------------------------- </br>"

    elif request.method=="POST":
        if len(Museo.objects.all())==0:
            parserXML('./museos/museos.xml')
        content_title ="Museos cargados"
        museos = Museo.objects.all ()
        content = ""
        for museo in museos:
            museoid = str(museo.identidad)
            content += "<br><a href='/" + museoid + "'>"
            content += museo.nombre + "</a><br>"
            content += "<br><li>URL del sitio: </li> <a href='" + museo.url +"'> " + museo.url + "</a></br>"
            content += "<br> ---------------------------------------------------------------------------------------------------------------------------------------- </br>"


    c = Context({'inicio': inicio, 'registro': registro, 'content_title': content_title, 'content': content})
    template = get_template ('museos.html')
    respuesta = template.render(c)
    return HttpResponse(respuesta)

@csrf_exempt
def main(request):
    if len(Museo.objects.all())==0:
        content_title ="Aún no hay museos cargados"
        content = "<form action='/' method='post'>"
        content += "<button type='submit'>CARGAR</button>"
        content += "</form>"
    else:
        content_title="5 museos más comentados"
        content=""

    if request.method =="GET":
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


        museos = Museo.objects.order_by('-num_comentarios')
        limite=0
        for museo in museos:
            if not museo.num_comentarios==0:
                content += "<a href=museos/" + museo.identidad + "><p>" + str(museo.nombre) + "</p>"
                limite=limite+1;
                if limite == 5:
                    break

    elif request.method == "POST":
        if len(Museo.objects.all()) == 0:
            parserXML('./museos/museos.xml')
            return redirect("/")

    user=str(request.user.username)
    c = Context({'inicio':  inicio, 'registro': registro, 'user': user, 'content_title':content_title, 'content': content})
    template = get_template ('home.html')
    respuesta = template.render(c)
    return HttpResponse(respuesta)
