from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from .models import Museo
from .parser import parserXML
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy

# Create your views here.
@csrf_exempt
def pos_list(request):
    if request.method =="GET":
        respuesta = "<br>Actualizar Datos<br>"
        respuesta += "<form action='/' method='post'>"
        respuesta += "<input type= 'hidden' name='opcion' value='1'>"
        respuesta += "<input type= 'submit' value='Actualizar'>"
        respuesta += "</form>"

    elif request.method == "POST":
        if len(Museo.objects.all()) == 0:
            parserXML('./museos/museos.xml')
            return redirect("/")
        respuesta = "<br> Datos actualizados <br>"

    museos = Museo.objects.all()
    c = Context({'content':  respuesta, 'museos': museos})
    template = get_template ('index.html')
    respuesta = template.render(c)
    return HttpResponse(respuesta)
