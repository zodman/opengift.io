# -*- coding:utf-8 -*-
__author__ = 'Tonakai'

from django.http import Http404
from django.template.loader_tags import register
from PManager.models.users import PM_User, PM_ProjectRoles, PM_Role
from PManager.models.tasks import PM_Project, PM_Task, PM_Task_Status
import datetime


@register.simple_tag()
def multiply(position, width, *args, **kwargs):
    return position * width


@register.inclusion_tag('kanban/templates/task.html')
def show_micro_task(task):
    return {
        'id': task.id,
        'name': task.name,
        'status': task.status.code,
        'executor': task.resp.get_profile().avatar_rel if task.resp else '',
        'executor_id': task.resp.id if task.resp else '',
        'deadline': task.deadline
    }

def widget(request, headerValues, widgetParams={}, qArgs=[]):
    user = request.user
    current_project = headerValues['CURRENT_PROJECT']

    if current_project:
        projects = [current_project]
    else:
        projects = user.get_profile().getProjects()
    statuses = PM_Task_Status.objects.all().order_by('-id')
    tasks = PM_Task.objects.filter(project__in=projects, closed=False, onPlanning=False, status__in=statuses)
    projects_data = {}
    for task in tasks:
        idx = str(task.project.id)
        if idx not in projects_data:
            print 'not have attribute'
            projects_data[idx] = {
                'project': task.project,
                'date_init': task.project.dateCreate,
                'user_source': task.project.getUsers(),
                'tasks': []
            }
        projects_data[idx]['tasks'].append(task)
    prd_array = []
    for pd in projects_data:
        prd_array.append(projects_data[pd])
    return {
        'projects_data': prd_array,
        'statuses': statuses,
        'status_width': 100 / statuses.count() if statuses.count() != 0 else 100,
        'status_width_remains': 100 % statuses.count() if statuses.count() != 0 else 0
    }