# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from django.shortcuts import render, HttpResponseRedirect
import time
from robokassa.forms import RobokassaForm

def paysystems(request):
    return render(request, 'robokassa/info.html', {'result': request})

def payment(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')#TODO:перенести в одно место

    form = RobokassaForm(initial={
           'OutSum': 900,#order.total,
           'InvId': request.user.id + int(time.time()),#order.id,
           'Desc': 'Premium аккаунт Heliard',#order.name,
           'Email': request.user.email,
           'user': request.user.id
           # 'IncCurrLabel': '',
           # 'Culture': 'ru'
       })
    return render(request, 'robokassa/payment.html', {'request': request, 'form': form})