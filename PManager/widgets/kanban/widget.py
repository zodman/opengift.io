# -*- coding:utf-8 -*-
__author__ = 'Tonakai'

from django.http import Http404
from django.template.loader_tags import register
from PManager.models.users import PM_User, PM_ProjectRoles, PM_Role
from PManager.models.tasks import PM_Project, PM_Task, PM_Task_Status
from PManager.viewsExt.tasks import TaskWidgetManager
from PManager.widgets.tasklist.widget import get_task_tag_rel_array, get_user_tag_sums
import datetime, json
from django.db import transaction


@transaction.commit_manually
def flush_transaction():
    transaction.commit()

@register.simple_tag()
def multiply(position, width, *args, **kwargs):
    return position * width


@register.inclusion_tag('kanban/templates/task.html')
def show_micro_task(task):
    avatar = False
    if not task:
        return False
    if task.resp:
        avatar = task.resp.get_profile().avatar_rel
        avatar['size'] = 30
    return {
        'id': task.id,
        'name': task.name if task.name else '',
        'url': task.url,
        'status': task.status.code if task.status else '',
        'executor': json.dumps(avatar) if avatar else '',
        'executor_id': task.resp.id if task.resp else '',
        'deadline': task.deadline if task.deadline else ''
    }

def widget(request, headerValues, widgetParams={}, qArgs=[]):
    flush_transaction()
    widgetManager = TaskWidgetManager()
    user = request.user
    current_project = headerValues['CURRENT_PROJECT'].id if headerValues['CURRENT_PROJECT'] else None
    statuses = PM_Task_Status.objects.all().order_by('-id')
    statuses_flat = statuses.values_list('id', flat=True)
    filter = dict(closed=False, onPlanning=False, status__in=statuses_flat)
    if current_project:
        filter['project'] = current_project

    tasks = PM_Task.getForUser(user, current_project, filter, [], {
            'order_by': [
                '-id'
            ]
        })
    projects_data = {}
    recommended_user = None
    for task in tasks['tasks']:
        idx = str(task.project.id)
        if idx not in projects_data:
            projects_data[idx] = {
                'project': task.project,
                'date_init': task.project.dateCreate,
                'user_source': task.project.getUsers(),
                'tasks': []
            }

        #todo: две строки ниже используются в трех местах, обхединить в метод, когда будет время
        aUsersHaveAccess = widgetManager.getResponsibleList(request.user, None).values_list('id', flat=True)
        recommended_user, tags = get_user_tag_sums(get_task_tag_rel_array(task), recommended_user, aUsersHaveAccess)

        task_data = {'task': task, 'responsibleList': tags}
        projects_data[idx]['tasks'].append(task_data)
    prd_array = []
    for pd in projects_data:
        prd_array.append(projects_data[pd])
    return {
        'projects_data': prd_array,
        'statuses': statuses,
        'status_width': 100 / statuses.count() if statuses.count() != 0 else 100,
        'status_width_remains': 100 % statuses.count() if statuses.count() != 0 else 0,
    }