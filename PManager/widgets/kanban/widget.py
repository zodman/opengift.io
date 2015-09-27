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

def widget(request, headerValues, widgetParams={}, qArgs=[]):
    flush_transaction()
    widgetManager = TaskWidgetManager()
    user = request.user
    current_project = headerValues['CURRENT_PROJECT'].id if headerValues['CURRENT_PROJECT'] else None
    filter = dict(closed=False, onPlanning=False)


    statuses = [status.__dict__ for status in PM_Task_Status.objects.all().order_by('-id')]

    curProject = None
    if current_project:
        try:
            curProject = PM_Project.objects.get(id=current_project)
        except Exception:
            pass

    arColorsByProject = {}

    colors = PM_Task.colors

    if curProject:
        projects = [curProject]
    else:
        projects = user.get_profile().getProjects()

    for project in projects:
        projectSettings = project.getSettings()
        aColumns = []
        if projectSettings.get('use_colors_in_kanban', False):
            for color_code, color in colors:
                settingColor = 'color_name_' + color_code
                if settingColor in projectSettings and projectSettings[settingColor]:

                    aColumns.append({'code': color_code, 'name': projectSettings[settingColor], 'prop': 'color'})
        else:
            for status in statuses:
                status.update({'prop': 'status'})
                aColumns.append(status)

        setattr(project, 'columns', aColumns)
        setattr(project, 'date_init', project.dateCreate)
        setattr(project, 'user_source', project.getUsers())
        setattr(project, 'status_width', 100 / len(aColumns) - 2 if len(aColumns) != 0 else 100)
        setattr(project, 'status_width_remains', 100 % len(aColumns) if len(aColumns) != 0 else 0)

    # else:
    #     filter['status__in'] = [status['id'] for status in statuses]

    # tasks = PM_Task.getForUser(user, current_project, filter, [], {
    #         'order_by': [
    #             '-id'
    #         ]
    #     })
    #
    # tasks['tasks'] = tasks['tasks'][:100]
    # projects_data = {}
    # recommended_user = None
    #aUsersHaveAccess = widgetManager.getResponsibleList(request.user, None).values_list('id', flat=True)

    # for task in tasks['tasks']:
    #     idx = str(task.project.id)
    #     statuses_is_colors = task.project.id in arColorsByProject
    #
    #     if idx not in projects_data:
    #         projectStatuses = arColorsByProject[task.project.id] if statuses_is_colors else statuses
    #         projects_data[idx] = {
    #             'statuses': projectStatuses,
    #             'project': task.project,
    #             'date_init': task.project.dateCreate,
    #             'user_source': task.project.getUsers(),
    #             'status_width': 100 / len(projectStatuses) - 2 if len(projectStatuses) != 0 else 100,
    #             'status_width_remains': 100 % len(projectStatuses) if len(projectStatuses) != 0 else 0,
    #             'tasks': []
    #         }
    #     statusCode = task.status.code if task.status else ''
    #     taskStatus = task.color if statuses_is_colors else statusCode
    #     if taskStatus not in [status['code'] for status in projects_data[idx]['statuses']]:
    #         continue
    #
    #     #todo: две строки ниже используются в трех местах, обхединить в метод, когда будет время
    #
    #     recommended_user, tags = get_user_tag_sums(get_task_tag_rel_array(task), recommended_user, aUsersHaveAccess)
    #
    #
    #     setattr(task, 'kanbanStatus', taskStatus)
    #     setattr(task, 'status_is_color', int(statuses_is_colors))
    #
    #     task_data = {
    #         'task': task,
    #         'responsibleList': tags
    #     }
    #
    #     projects_data[idx]['tasks'].append(task_data)

    # prd_array = []
    # for pd in projects_data:
    #     prd_array.append(projects_data[pd])

    return {
        'projects_data': projects,
        'title': u'Канбан',
        'current_project': curProject,
        'arColorsByProject': arColorsByProject
    }