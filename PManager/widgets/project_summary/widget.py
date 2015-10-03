# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from PManager.models import PM_Timer, PM_Task, Credit
import datetime


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

        projectDebt = 0
        for o in Credit.objects.raw(
                'SELECT sum(value) as summ, id, project_id from PManager_credit' +
                ' WHERE `payer_id` IS NOT NULL AND value > 0'
                ' AND `project_id`=' + str(int(project.id))
            ):
            projectDebt += o.summ if o.summ else 0

        projectDebtPayed = 0
        for o in Credit.objects.raw(
                'SELECT sum(value) as summ, id, project_id from PManager_credit' +
                ' WHERE `user_id` IS NOT NULL AND value < 0'
                ' AND `project_id`=' + str(int(project.id))
            ):
            projectDebtPayed += o.summ if o.summ else 0

        setattr(project, 'projectSum', projectSum)
        setattr(project, 'projectSumPayed', projectSumPayed)
        setattr(project, 'projectDebt', projectDebt)
        setattr(project, 'projectDebtPayed', projectDebtPayed)

    return {
        'projects':projects,
        'title': u'Сводка по проектам'
    }