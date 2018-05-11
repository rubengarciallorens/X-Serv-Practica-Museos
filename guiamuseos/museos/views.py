from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from .models import Museo

# Create your views here.

def pos_list(request):
    if request.method =="GET":
        if len(Museo.objects.all()) == 0:
            respuesta = "No hay datos disponibles en la base de datos"
            form1 = "<br>Actualizar Datos<br>"
            form1 += "<form action='/' method='post'>"
            form1 += "<input type= 'hidden' name='opcion' value='1'>"
            form1 += "<input type= 'submit' value='Actualizar'>"
            form1 += "</form>"
        else:
            form1 = "<br>Mostrar los accesibles<br>"
            form1 += "<form action='/' method='post'>"
            form1 += "<input type= 'hidden' name='opcion' value='2'>"
            form1 += "<input type= 'submit' value='Mostrar'>"
            form1 += "</form>"

    elif request.method == "POST":
        opcion = request.POST['opcion']
        if opcion == "1":
            parser(request)
            return redirect("/")

        c = Context({'content': respuesta, 'filtro': form1})
        template = get_template ('index.html')
        respuesta = template.render(c)
        return HttpResponse(respuesta)
