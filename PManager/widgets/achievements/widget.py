# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from PManager.models import PM_Timer
from PManager.viewsExt.tools import templateTools

def widget(request,headerValues,ar,qargs):
    allTimers = PM_Timer.objects.filter(user=request.user.id).all()
    allTime = 0
    for timer in allTimers:
        if timer.seconds:
            allTime += int(timer.seconds)

    return {'allTime':templateTools.dateTime.timeFromTimestamp(allTime)}