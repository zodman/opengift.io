# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from PManager.models import PM_Task

def widget(request, headerValues, ar, qargs):
    current_project = headerValues['CURRENT_PROJECT']
    bPay = request.POST.get('pay', False)
    summ = int(request.POST.get('summ', 0) or 0)

    profile = request.user.get_profile()

    total = profile.account_total or 0
    if current_project:
        bet = profile.getBet(current_project)
        if bet:
            bet = bet - (profile.rating or 0)
    else:
        bet = profile.sp_price

    projectData = {
        'allProjectPrice': total,
        'closedTasksQty': int(PM_Task.getQtyForUser(request.user, None, {'closed': True, 'active': True})),
        'tasksQty': int(PM_Task.getQtyForUser(request.user, None, {'closed': False, 'active': True})),
        'bPay': bPay,
        'rating': profile.rating or 0 if not profile.isClient(current_project) else 0,
        'rate': bet if bet else 0,
        'premiumTill': profile.premium_till or '01.06.2015' if request.user.is_staff else ''
    }

    return projectData