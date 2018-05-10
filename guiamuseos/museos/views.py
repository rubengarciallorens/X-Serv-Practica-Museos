from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template

# Create your views here.

def pos_list(request):
    if request.method =="GET":
        template = get_template ('index.html')
        return HttpResponse(template.render)
