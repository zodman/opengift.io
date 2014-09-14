# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from PManager.models import PM_Task
import datetime


def widget(request,headerValues,a,b):
    projects = request.user.get_profile().managedProjects
    for project in projects:
        readyTaskQty = PM_Task.objects.filter(project=project,status__code='ready',closed=False).count()
        overdueTaskQty = PM_Task.objects.filter(project=project,deadline__lt=datetime.datetime.now(),closed=False).count()

        setattr(project,'readyTaskQty',readyTaskQty)
        setattr(project,'overdueTaskQty',overdueTaskQty)

    return {
        'projects':projects
    }