# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from PManager.models import PM_Timer, PM_Task, Credit
import datetime
from django.db.models import Sum

def widget(request, headerValues, a, b):
    projects = request.user.get_profile().managedProjects
    for project in projects:
        projectSum = 0
        for o in Credit.objects.raw(
                'SELECT sum(value) as summ, id, project_id from PManager_credit' +
                ' WHERE `user_id` IS NOT NULL AND value > 0'
                ' AND `project_id`=' + str(int(project.id))
            ):
            projectSum += o.summ if o.summ else 0

        projectSumPayed = 0
        for o in Credit.objects.raw(
                'SELECT sum(value) as summ, id, project_id from PManager_credit' +
                ' WHERE `user_id` IS NOT NULL AND value < 0'
                ' AND `project_id`=' + str(int(project.id))
            ):
            projectSumPayed += o.summ if o.summ else 0

        tasks = PM_Task.objects.filter(project=project, closed=False).aggregate(Sum('planTime'))
        realtime = PM_Timer.objects.filter(task__project=project, task__closed=False).aggregate(Sum('seconds'))
        realtime = realtime['seconds__sum'] or 0
        plantime = tasks['planTime__sum'] or 0

        setattr(project, 'projectSum', projectSum)
        setattr(project, 'projectSumPayed', projectSumPayed)
        setattr(project, 'realtime', round(realtime/3600.0, 2))
        setattr(project, 'plantime', plantime)

    return {
        'projects':projects,
        'title': u'Сводка по проектам'
    }