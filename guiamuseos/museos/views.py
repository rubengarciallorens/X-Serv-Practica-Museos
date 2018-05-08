from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def pos_list(request):
    return render(request, 'post_list.html')
