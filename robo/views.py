__author__ = 'Gvammer'
from django.shortcuts import render

def paysystems(request):
    return render(request, 'robokassa/info.html', {'result': request})