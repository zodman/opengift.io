# -*- coding:utf-8 -*-
__author__ = 'Tonakai'
from django.http import Http404
from PManager.models.users import PM_User
from PManager.models.tasks import PM_Task_Status, PM_Task, PM_Milestone
from PManager.services.access import project_access
import json, copy, datetime

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
        newStatus = False
        for status in statuses:
            status.update({'prop': 'status'})
            if status['code'] == 'revision':
                status['name'] = u'В работе'

                newStatus = copy.copy(status)
                newStatus['code'] = 'closed'
                newStatus['name'] = u'Закрыта'

            columns.append(status)
        if newStatus:
            columns.append(newStatus)

    return (columns, projectSettings.get('use_colors_in_kanban', False))

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
        (columns, use_colors) = project_columns(project, colors, statuses)
        project_to_kanban_project(project, columns)
        setattr(project, 'use_colors', use_colors)

        current_milestone = None
        if request.GET.get('milestone', False):
            current_milestone = PM_Milestone.objects.filter(project=project, pk=int(request.GET.get('milestone', 0)))
        else:
            current_milestone = PM_Milestone.objects.filter(
                closed=False,
                date__gt=datetime.datetime.now(),
                project=project
            ).order_by('date')

        if current_milestone:
            current_milestone = current_milestone[0]
            setattr(project, 'current_milestone', current_milestone)


    return {
        'projects_data': projects,
        'title': u'Канбан',
        'current_project': current_project,
        'use_colors': use_colors,
        'arColorsByProject': arColorsByProject
    }
