from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from .models import Museo, Comentario, Museo_añadido, Seleccion
from .parser import parserXML
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import timezone

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy

# Create your views here.

solo_museos = 0

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
    titulo = "Página de " + str(username)
    pagina_personal = Seleccion (propietario=str(username), nombre = titulo)
    pagina_personal.save()
    return HttpResponseRedirect("/")

@csrf_exempt
def personal (request, propietario):
    global solo_museos
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
        registro +="<br> Esperamos que su visita a la página sea satisfactoria"

    if request.method == "GET":
        seleccion = Seleccion.objects.get (propietario = propietario)
        favoritos = seleccion.museos_fav.all()
        content_title=seleccion.nombre
        content=""
        for favorito in favoritos:
            if solo_museos==0:
                content += "<br><li><a href='" + favorito.museo.url + "'><p>" + str(favorito.museo.nombre) + ":</p></a></li></br>"
                content += "<br>Dirección: " + favorito.museo.localizacion +"</br>"
                content += "<br><a href=museos/" + favorito.museo.identidad + "><p> Más información</p></a></br>"
                content+="<br><p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Añadido: " + str(favorito.añadido) + "</br></p>"
            elif solo_museos==1:
                if favorito.museo.accesibilidad=='1':
                    content += "<br><li><a href='" + favorito.museo.url + "'><p>" + str(favorito.museo.nombre) + ":</p></a></li></br>"
                    content += "<br>Dirección: " + favorito.museo.localizacion +"</br>"
                    content += "<br><a href=museos/" + favorito.museo.identidad + "><p> Más información</p></a></br>"
                    content+="<br><p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Añadido: " + str(favorito.añadido) + "</br></p>"

        if len(favoritos)!=0:
            content += "<li><a href='/" + propietario + "/XML'>"
            content += "XML</a></li>" 
    
    elif request.method =="POST" and request.POST['opcion']=='1':
        seleccion = Seleccion.objects.get (propietario = propietario)
        seleccion.nombre = request.POST['texto']
        seleccion.save()
        favoritos = seleccion.museos_fav.all()
        content_title=seleccion.nombre
        content=""
        for favorito in favoritos:
            if solo_museos==0:
                content += "<br><li><a href='" + favorito.museo.url + "'><p>" + str(favorito.museo.nombre) + ":</p></a></li></br>"
                content += "<br>Dirección: " + favorito.museo.localizacion +"</br>"
                content += "<br><a href=museos/" + favorito.museo.identidad + "><p> Más información</p></a></br>"
                content+="<br><p> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Añadido: " + str(favorito.añadido) + "</br></p>"
            elif solo_museos==1:
                if favorito.museo.accesibilidad=='1':
                    content += "<br><li><a href='" + favorito.museo.url + "'><p>" + str(favorito.museo.nombre) + ":</p></a></li></br>"
                    content += "<br>Dirección: " + favorito.museo.localizacion +"</br>"
                    content += "<br><a href=museos/" + favorito.museo.identidad + "><p> Más información</p></a></br>"
                    content+="<br><p> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Añadido: " + str(favorito.añadido) + "</br></p>"

        if len(favoritos)!=0:
            content += "<li><a href='/" + propietario + "/XML'>"
            content += "XML</a></li>"
     
    
    if request.user.is_authenticated() and request.user.username == propietario:

        personales = "<form action='/" + propietario + "' method=POST>"
        personales += "Cambiar nombre de tu página personal<input type= 'text' name='texto'>"
        personales += "<input type= 'hidden' name='opcion' value='1'>"
        personales += "<input type= 'submit' value='Cambiar'>"
        personales += "</form>"

        registro = "<li> Personalizar color fondo (en ocasiones será necesario recargar la página para que se apliquen los cambios)</li>"
        registro += "<br><form action='/css_color' method=GET>"
        registro += "<select name='Colores de fondo'>"
        registro += "<option value=Blanco> Blanco</option>"
        registro += "<option value=Crema> Crema</option>"
        registro += "<option value=Plata> Plata</option>"
        registro += "<input type= 'submit' value='FILTRAR'>"
        registro += "</form></br>"

        registro += "<li> Cambiar tamaño letra (en ocasiones será necesario recargar la página para que se apliquen los cambios) </li>"
        registro += "<br><form action='/css_letra' method=GET>"
        registro += "<select name='Tamaño letra cuerpo página'>"
        registro += "<option value=Pequeña> Pequeña</option>"
        registro += "<option value=Mediana> Mediana</option>"
        registro += "<option value=Grande> Grande</option>"
        registro += "<input type= 'submit' value='FILTRAR'>"
        registro += "</form></br>"

    else:
        pag_personales = Seleccion.objects.all()
        personales = ""
        for pag_personal in pag_personales:
            personales += "<br><a href='/" + pag_personal.propietario + "'>"
            personales += pag_personal.nombre + "</a></br>"
    
    user=str(request.user.username)
    personales_title="Páginas personales"

    todos_comentarios = Comentario.objects.all()
    maximo = len(todos_comentarios) - 5
    num=0
    if len(todos_comentarios)!=0:
        comentarios =""
        for comentario in todos_comentarios:
            if num >= maximo:
                comentarios += "<li>" + comentario.museo.nombre + ":</li>"
                comentarios += "<p>&nbsp&nbsp&nbsp&nbsp" + comentario.texto + "</p>"
            num = num+1

    c = Context({'inicio': inicio, 'user': user, 'registro': registro, 'personales_title': personales_title, 'personales':personales, 'content_title': content_title, 'content': content, 'comentarios':comentarios})
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
        registro +="<br> Esperamos que su visita a la página sea satisfactoria"

    museo=Museo.objects.get(identidad=id)
    content_title = str(museo.nombre)

    if request.method=="POST" and request.POST['opcion']=='1':
        texto = request.POST['texto']
        comentario = Comentario (museo = museo , texto= texto)
        comentario.save()
        museo.num_comentarios=museo.num_comentarios + 1
        museo.save()
    if request.method=="POST" and request.POST['opcion']=='2':
        museo_añadido = Museo_añadido (museo = museo, añadido = timezone.now())
        museo_añadido.save()
        seleccion = Seleccion.objects.get (propietario = request.user.username)
        favoritos = seleccion.museos_fav.all()
        if favoritos.filter(museo=museo_añadido.museo).count() == 0:
            seleccion.museos_fav.add(museo_añadido)
            seleccion.save()

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

        content += "<br><form action='/museos/" + str(id) + "' method=POST>"
        content += "<input type= 'hidden' name='opcion' value='2'>"
        content += "<input type= 'submit' value='Añadir a mi página personal'>"
        content += "</form></br>"

    if not request.user.is_authenticated():
        content += "<br><li>Podrá añadir comentarios cuando se registre en la página y se identifique. </li>"
    user=str(request.user.username)
    pag_personales = Seleccion.objects.all()
    personales = ""
    for pag_personal in pag_personales:
        personales += "<br><a href='/" + pag_personal.propietario + "'>"
        personales += pag_personal.nombre + "</a></br>"
    personales_title="Páginas personales"

    todos_comentarios = Comentario.objects.all()
    maximo = len(todos_comentarios) - 5
    num=0
    if len(todos_comentarios)!=0:
        comentarios =""
        for comentario in todos_comentarios:
            if num >= maximo:
                comentarios += "<li>" + comentario.museo.nombre + ":</li>"
                comentarios += "<p>&nbsp&nbsp&nbsp&nbsp" + comentario.texto + "</p>"
            num = num+1

    c = Context({'inicio': inicio, 'registro': registro,'personales_title':personales_title,
     'personales':personales, 'user': user, 'content_title': content_title, 'content': content, 'comentarios':comentarios})
    template = get_template ('museo_pers.html')
    respuesta = template.render(c)
    return HttpResponse(respuesta)

@csrf_exempt
def allmuseums(request):
    global solo_museos
    if not request.user.is_authenticated():
        inicio = "<form action='/login' method='post'>"
        inicio += "<label for='username'>Username:</label>"
        inicio += "<input type='text' name='username'"
        inicio += "<label for='password'>Password:</label>"
        inicio += "<input type='password' name='password'>"

        inicio += "<input type='submit' value='LOGIN' />"
        inicio += "</form>"

        registro = "<form action='register/' method='post'>"
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
        registro +="<br> Esperamos que su visita a la página sea satisfactoria"

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
                if solo_museos ==0:
                    museoid = str(museo.identidad)
                    content += "<br><a href=museos/" + museoid + ">"
                    content += museo.nombre + "</a><br>"
                    content += "<br><li>URL del sitio: </li> <a href='" + museo.url +"'> " + museo.url + "</a></br>"
                    content += "<br> ---------------------------------------------------------------------------------------------------------------------------------------- </br>"
                elif solo_museos ==1:
                    if museo.accesibilidad=='1':
                        museoid = str(museo.identidad)
                        content += "<br><a href=museos/" + museoid + ">"
                        content += museo.nombre + "</a><br>"
                        content += "<br><li>URL del sitio: </li> <a href='" + museo.url +"'> " + museo.url + "</a></br>"
                        content += "<br> ---------------------------------------------------------------------------------------------------------------------------------------- </br>"

    elif request.method=="POST":
        if len(Museo.objects.all())==0:
            parserXML('./museos/museos.xml')
        content_title ="Todos los museos cargados"
        museos = Museo.objects.all ()
        content = ""
        if len(Museo.objects.all())==0:
            for museo in museos:
                if solo_museos==0:
                    museoid = str(museo.identidad)
                    content += "<br><a href='/" + museoid + "'>"
                    content += museo.nombre + "</a><br>"
                    content += "<br><li>URL del sitio: </li> <a href='" + museo.url +"'> " + museo.url + "</a></br>"
                    content += "<br> ---------------------------------------------------------------------------------------------------------------------------------------- </br>"
                elif solo_museos ==1:
                    if museo.accesibilidad=='1':
                        museoid = str(museo.identidad)
                        content += "<br><a href='/" + museoid + "'>"
                        content += museo.nombre + "</a><br>"
                        content += "<br><li>URL del sitio: </li> <a href='" + museo.url +"'> " + museo.url + "</a></br>"
                        content += "<br> ---------------------------------------------------------------------------------------------------------------------------------------- </br>"
        else:
            dist_ele = request.body.decode('utf-8').split("=")[1] #Saca el valor del distrito del POST mandado por la opcion de filtrar
            distrito = str(dist_ele)
            for museo in museos:
                if solo_museos==0:
                    if distrito == str(museo.distrito):
                        museoid = str(museo.identidad)
                        content += "<br><a href='/museos/" + museoid + "'>"
                        content += museo.nombre + "</a><br>"
                        content += "<br><li>URL del sitio: </li> <a href='" + museo.url +"'> " + museo.url + "</a></br>"
                        content += "<br> ---------------------------------------------------------------------------------------------------------------------------------------- </br>"
                elif solo_museos==1:
                    if museo.accesibilidad=='1':
                        museoid = str(museo.identidad)
                        content += "<br><a href='/museos/" + museoid + "'>"
                        content += museo.nombre + "</a><br>"
                        content += "<br><li>URL del sitio: </li> <a href='" + museo.url +"'> " + museo.url + "</a></br>"
                        content += "<br> ---------------------------------------------------------------------------------------------------------------------------------------- </br>"

    museos_distritos= Museo.objects.all()
    distritos = museos_distritos.values_list('distrito', flat=True).distinct()
    personales = "<form action='/museos' method='post'>"
    personales += "<select name='Distrito'>"
    for distrito in distritos:
        personales += "<option value='" + distrito + "'>" + distrito
        personales += "</option>"
    if len(Museo.objects.all())!=0:
        personales += "<input type= 'submit' value='FILTRAR'>"
    else:
        personales += "<input type= 'submit' value='CARGAR MUSEOS'>"
    personales += "</form>"

    user=str(request.user.username)
    personales_title="Filtrar por distrito"

    todos_comentarios = Comentario.objects.all()
    maximo = len(todos_comentarios) - 5
    num=0
    if len(todos_comentarios)!=0:
        comentarios =""
        for comentario in todos_comentarios:
            if num >= maximo:
                comentarios += "<li>" + comentario.museo.nombre + ":</li>"
                comentarios += "<p>&nbsp&nbsp&nbsp&nbsp" + comentario.texto + "</p>"
            num = num+1          
    
    c = Context({'inicio': inicio, 'personales_title': personales_title, 'personales': personales, 'registro': registro, 'user': user, 'content_title': content_title, 'content': content, 'comentarios':comentarios})
    template = get_template ('museos.html')
    respuesta = template.render(c)
    return HttpResponse(respuesta)

@csrf_exempt
def main(request):

    global solo_museos
    if solo_museos == 0:
        accesibilidad ="Mostrar solo museos"
    elif solo_museos == 1:
        accesibilidad = "Mostrar todos los establecimientos tengan accesibilidad 1 o no"

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
            registro +="<br> Esperamos que su visita a la página sea satisfactoria"


        museos = Museo.objects.order_by('-num_comentarios')
        limite=0
        for museo in museos:
            if not museo.num_comentarios==0:
                if solo_museos == 0:
                    content += "<li><a href='" + museo.url + "'><p>" + str(museo.nombre) + ":</p></a></li>"
                    content += "<br>Dirección: " + museo.localizacion +"</br>"
                    content += "<br><a href=museos/" + museo.identidad + "><p> Más información</p></a></br>"
                    limite=limite+1;
                    if limite == 5:
                        break
                elif solo_museos ==1:
                    if museo.accesibilidad=='1':
                        content += "<li><a href='" + museo.url + "'><p>" + str(museo.nombre) + ":</p></a></li>"
                        content += "<br>Dirección: " + museo.localizacion +"</br>"
                        content += "<br><a href=museos/" + museo.identidad + "><p> Más información</p></a></br>"
                        limite=limite+1;
                        if limite == 5:
                            break
        pag_personales = Seleccion.objects.all()
        personales = ""
        for pag_personal in pag_personales:
            personales += "<br><a href='/" + pag_personal.propietario + "'>"
            personales += pag_personal.nombre + "</a></br>"

    elif request.method == "POST":
        if len(Museo.objects.all()) == 0:
            parserXML('./museos/museos.xml')
            return redirect("/")

    user=str(request.user.username)
    personales_title="Páginas personales"
    global solo_museos
    if solo_museos == 0:
        accesibilidad ="Mostrar solo museos"
    elif solo_museos == 1:
        accesibilidad = "Mostrar todos emplazamientos"

    
    todos_comentarios = Comentario.objects.all()
    maximo = len(todos_comentarios) - 5
    num=0
    if len(todos_comentarios)!=0:
        comentarios =""
        for comentario in todos_comentarios:
            if num >= maximo:
                comentarios += "<li>" + comentario.museo.nombre + ":</li>"
                comentarios += "<p>&nbsp&nbsp&nbsp&nbsp" + comentario.texto + "</p>"
            num = num+1

    c = Context({'inicio':  inicio, 'registro': registro, 'personales_title': personales_title, 'personales': personales,
                 'user': user, 'content_title':content_title, 'content': content, 'accesibilidad': accesibilidad, 'comentarios':comentarios})
    template = get_template ('home.html')
    respuesta = template.render(c)
    return HttpResponse(respuesta)

def css_color (request): 

    color = request.GET['Colores de fondo']
    css_old = open ('museos/static/css/templatemo_style.css', 'r') #Lo utilizo para saber las filas del css
    lines = []
    for line in css_old:
        lines.append(line)
    css_old.close()

    css_new = open ('museos/static/css/templatemo_style.css', 'w') #Lo utilizo para saber las filas del css
    maximo = 0
    for line in lines:
        if color != 'None':
            if maximo == 11:    #Aquí está la línea del background
                if color == 'Crema':
                    line = "background: #F3E2A9;\n"
                elif color == 'Blanco':
                    line = "background: #FFFFFF;\n"
                elif color == 'Plata':
                    line = "background: #E6E6E6;\n"
        maximo=maximo+1
        css_new.write(line)

    css_new.close()

    return HttpResponseRedirect("/")

def css_letra (request):
    letra = request.GET['Tamaño letra cuerpo página']
    css_old = open ('museos/static/css/templatemo_style.css', 'r') #Lo utilizo para saber las filas del css
    lines = []
    for line in css_old:
        lines.append(line)
    css_old.close()

    css_new = open ('museos/static/css/templatemo_style.css', 'w') #Lo utilizo para saber las filas del css
    maximo = 0
    for line in lines:
        if letra != 'None':
            if maximo == 18:    #Aquí está la línea del background
                if letra == 'Pequeña':
                    line = "font-size: 8px;\n"
                elif letra == 'Mediana':
                    line = "font-size: 12px;\n"
                elif letra == 'Grande':
                    line = "font-size: 16px;\n"
        maximo=maximo+1
        css_new.write(line)

    css_new.close()
    return HttpResponseRedirect("/")

def XML(request, propietario):
    seleccion = Seleccion.objects.get(propietario=propietario)
    museos = seleccion.museos_fav.all()
    respuesta = "<?xml version='1.0' encoding='UTF-8'?>\n"
    respuesta += "<Contenidos>"
    for museo in museos:
        respuesta += "<contenido>"
        respuesta += "<atributo nombre='ID-ENTIDAD'>" + museo.museo.identidad + "</atributo>"
        respuesta += "<atributo nombre='NOMBRE'>" + museo.museo.nombre + "</atributo>"
        respuesta += "<atributo nombre='EQUIPAMIENTO'>" + museo.museo.equipamiento + "</atributo>"
        respuesta += "<atributo nombre='TRANSPORTE'>" + museo.museo.transporte + "</atributo>"
        respuesta += "<atributo nombre='DESCRIPCION'>" + museo.museo.descripcion + "</atributo>"
        respuesta += "<atributo nombre='HORARIO'>" + museo.museo.horario + "</atributo>"
        respuesta += "<atributo nombre='ACCESIBILIDAD'>" + museo.museo.accesibilidad + "</atributo>"
        respuesta += "<atributo nombre='LOCALIZACION'>" + museo.museo.localizacion + "</atributo>"
        respuesta += "<atributo nombre='DISTRITO'>" + museo.museo.distrito + "</atributo>"
        respuesta += "<atributo nombre='TELEFONO'>" + museo.museo.telefono + "</atributo>"
        respuesta += "<atributo nombre='FAX'>" + museo.museo.fax + "</atributo>"
        respuesta += "<atributo nombre='EMAIL'>" + museo.museo.email + "</atributo>"
        respuesta += "<atributo nombre='TIPO'>" + museo.museo.tipo + "</atributo>"
        respuesta += "<atributo nombre='NUM-COMENTARIOS'>" + str(museo.museo.num_comentarios) + "</atributo>"
        respuesta += "</contenido>"
    respuesta += "</Contenidos>"
    return HttpResponse(respuesta, content_type="text/xml")

def accesibilidad (request):
    if solo_museos == 1:
        global solo_museos
        solo_museos = 0 
    elif solo_museos == 0:
        global solo_museos
        solo_museos = 1
    return HttpResponseRedirect("/")

def about (request):
    respuesta = "<p> Práctica realizada por: </p>"
    respuesta += "<p> - Rubén García Llorens </p>"
    respuesta += "<p> - DNI : 49101460W </p>"
    respuesta += "<p> - Doble Grado Sistemas de Telecomunicaciones y ADE </p>"
    respuesta += "<p> Si es la primera vez que accedes al sitio, te aparecerá un boton para cargar los museos que llamara a la función parser para parsear el XML de la comunidad, y guardarlo en la base de datos. </p>"
    respuesta += "<p> Una vez realizado esto se tendrá acceso al sitio completo. </p>"
    respuesta += "<p> Para registrar a un usuario bastará con rellenar los campos de registro que se encuentran a la derecha y pulsar en registro </p>"
    respuesta += "<p> Esto registrará al usuario, que ya podrá entrar en su cuenta haciendo login en la esquina superior derecha</p>"
    respuesta += "<p> Una vez identificado, cuando vaya a los museos y entre en la página propia de alguno  (pinchando en Más información) podrá añadirlo a su página personal y añadir comentarios para el mismo, que serán anónimos </p>"
    respuesta += "<p> En la página personal del usuario verá los museos que ha añadido y podrá cambiar el nombre a la derecha de su página. También podrás acceder a un XML con tus museos favoritos pinchando en el enlace 'XML' </p>"
    respuesta += "<p> En caso de entrar en una página de la cual no eres propietario verás simplemente los museos añadidos pero no podrás cambiar el nombre ni obtener el HTML </p>"
    respuesta += "<p> En la página principal, abajo te aparecerá un enlace en Accesibilidad, que al pincharlo la página pasará a mostrar todos los museos de la base de datos, o en su defecto solo los que tienen accesibilidad=1, depende lo que esté mostrando en ese momento.</p>"
    respuesta += "<p> Para acceder a /about, abajo en el template pinchando en 'RubénGarcíaLlorens'</p>"
    respuesta += "<p> Además de las funciones obligatorias, está implementado el favicon, y abajo a la izquierda hay un feed que siempre muestra los últimos 5 comentarios añadidos"
    return HttpResponse(respuesta)
