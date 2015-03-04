# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from PManager.models import PM_Task#, PM_Timer, Payment, Credit
from robokassa.forms import RobokassaForm
from random import randint
#import time

def widget(request, headerValues, ar, qargs):
    current_project = headerValues['CURRENT_PROJECT']
    bPay = request.POST.get('pay', False)
    summ = int(request.POST.get('summ', 0) or 0)

    # if not current_project:
    #     return False

    profile = request.user.get_profile()

    total = profile.account_total or 0

    form = RobokassaForm(initial={
           'OutSum': summ,#order.total,
           'InvId': request.user.id * 1000000 + randint(1, 10000),#order.id,
           'Desc': 'Пополнение счета Heliard',#order.name,
           'Email': request.user.email,
           # 'IncCurrLabel': '',
           # 'Culture': 'ru'
       })
    projectData = {
        'payForm': form,
        'allProjectPrice': total,
        'closedTasksQty': int(PM_Task.getQtyForUser(request.user, None, {'closed': True, 'active': True})),
        'tasksQty': int(PM_Task.getQtyForUser(request.user, None, {'closed': False, 'active': True})),
        'bPay': bPay,
        'rate': profile.getBet(current_project),
        'premiumTill': profile.premium_till or '01.04.2014' if request.user.is_staff else ''
    }

    return projectData