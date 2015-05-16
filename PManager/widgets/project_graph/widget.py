# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from PManager.models import PM_Task
from PManager.services.task_drafts import draft_cnt

def widget(request, headerValues, ar, qargs):
    current_project = headerValues['CURRENT_PROJECT']
    bPay = request.POST.get('pay', False)
    summ = int(request.POST.get('summ', 0) or 0)

    profile = request.user.get_profile()

    total = profile.account_total or 0
    bet = profile.getBet(current_project)
    projectData = {
        'allProjectPrice': total,
        'closedTasksQty': int(PM_Task.getQtyForUser(request.user, None, {'closed': True, 'active': True})),
        'tasksQty': int(PM_Task.getQtyForUser(request.user, None, {'closed': False, 'active': True})),
        'bPay': bPay,
        'rating': profile.rating or 0,
        'rate': bet - profile.rating if bet else 0,
        'premiumTill': profile.premium_till or '01.06.2015' if request.user.is_staff else '',
        'taskdrafts_cnt': draft_cnt(request.user)
    }

    return projectData