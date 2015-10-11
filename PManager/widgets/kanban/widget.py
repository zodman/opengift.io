# -*- coding:utf-8 -*-
__author__ = 'Tonakai'
from django.http import Http404
from PManager.models.users import PM_User
from PManager.models.tasks import PM_Task_Status, PM_Task
from PManager.services.access import project_access

def get_projects(user, current_project):
    if current_project:
        if not project_access(current_project.id, user.id):
            raise Http404
        return [current_project]
    else:
        return user.get_profile().getProjects()

def project_columns(project, colors, statuses):
    projectSettings = project.getSettings()
    columns = []
    if projectSettings.get('use_colors_in_kanban', False):
        for color_code, color in colors:
            settingColor = 'color_name_' + color_code
            if settingColor in projectSettings and projectSettings[settingColor]:
                columns.append({'code': color_code, 'name': projectSettings[settingColor], 'prop': 'color'})
    else:
        for status in statuses:
            status.update({'prop': 'status'})
            if status['code'] == 'ready':
                newStatus = copy.copy(status)
                newStatus['code'] = 'today'
                newStatus['name'] = u'Сделаю сегодня'

                columns.append(newStatus)

            if status['code'] == 'revision':
                status['name'] = u'В работе'

            columns.append(status)
    return columns

def project_to_kanban_project(project, columns):
    setattr(project, 'columns', columns)
    setattr(project, 'date_init', project.dateCreate)
    setattr(project, 'user_source', project.getUsers())
    return project

def get_statuses():
    return [status.__dict__ for status in PM_Task_Status.objects.all().order_by('-id')]

def widget(request, headerValues, widgetParams={}, qArgs=[]):
    current_project = headerValues['CURRENT_PROJECT']
    statuses = get_statuses()
    # unknown purpose
    arColorsByProject = {}
    colors = PM_Task.colors
    # raising Http404 if user has no access to current_project
    projects = get_projects(request.user, current_project)
    for project in projects:
        columns = project_columns(project, colors, statuses)
        project_to_kanban_project(project, columns)

    return {
        'projects_data': projects,
        'title': u'Канбан',
        'current_project': current_project,
        'arColorsByProject': arColorsByProject
    }
