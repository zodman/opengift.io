# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from django.shortcuts import HttpResponse, render, HttpResponseRedirect
from PManager.models import PM_Milestone, PM_Project, PM_Task, PM_MilestoneChanges
from django.template import RequestContext
from PManager.viewsExt.tools import templateTools
from PManager.viewsExt import headers
from PManager.widgets.gantt.widget import create_milestone_from_post


class ajaxMilestoneManager:
    def __init__(self, request):
        self.request = request

    def getRequestValue(self, key):
        if key in self.request.POST:
            return self.request.POST[key]
        else:
            return None


def milestoneForm(request):
    return render(request, 'helpers/milestone_create.html', dict())


def ajaxMilestonesResponder(request):
    milestone = None
    responseText = 'bad query'
    name = request.POST.get('name', '')
    description = request.POST.get('description', '')
    user = request.user
    responsible_id = request.POST.get('responsible', 0)
    date = request.POST.get('date', None)
    date = templateTools.dateTime.convertToDateTime(date) if date else None
    id = request.POST.get('id', None)
    task_id = int(request.POST.get('task_id', 0))
    critically = request.POST.get('critically', 2)
    action = request.POST.get('action', None)
    if action and not user.is_authenticated():
        return HttpResponse('not authorized')

    project = None
    try:
        project = PM_Project.objects.get(
            pk=int(request.POST.get('project', 0)),
            closed=False,
            locked=False
        )
    except PM_Project.DoesNotExist:
        if id:
            try:
                milestone = PM_Milestone.objects.get(pk=id)
                project = milestone.project
            except PM_Milestone.DoesNotExist:
                project = None

    if action == 'remove':
        if id:
            try:
                milestone = PM_Milestone.objects.get(pk=id)
                milestone.closed = True
                milestone.save()
                responseText = 'removed'
            except PM_Milestone.DoesNotExist:
                pass
    elif action == 'add_task_to_milestone':
        milestone = None
        if id:
            milestone = PM_Milestone.objects.get(pk=id)

        task = PM_Task.objects.get(pk=task_id)
        if task.milestone:
            change = PM_MilestoneChanges(milestone=task.milestone, value=-(task.planTime or 0))
            change.save()

        task.milestone = milestone
        task.save()

        if milestone:
            change = PM_MilestoneChanges(milestone=milestone, value=(task.planTime or 0))
            change.save()

        responseText = 'added'
    elif name and project:
        if not milestone:
            milestone = None
        if id:
            try:
                milestone = PM_Milestone.objects.get(pk=id)
                milestone.name = name
                milestone.date = date
                milestone.description = description
                milestone.project = project
            except PM_Milestone.DoesNotExist:
                pass
        else:
            milestone = PM_Milestone(name=name, date=date, project=project, description=description)


        if milestone:
            if not user.is_authenticated() or not user.get_profile().isManager(project):
                milestone.is_request = True

            milestone.save()
            if responsible_id:
                milestone.responsible.clear()
                milestone.responsible.add(responsible_id)
            else:
                if user.is_authenticated():
                    milestone.responsible.add(user)
            responseText = milestone.id

    return HttpResponse(responseText)


def milestonesResponder(request, activeMenuItem=None):
    from PManager.viewsExt import headers

    headerValues = headers.initGlobals(request)
    create_milestone_from_post(request, headerValues)
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect('/')

    context = RequestContext(request)
    selected_project = context.get("CURRENT_PROJECT")
    if selected_project:
        mprojects = (selected_project,)
    else:
        mprojects = context.get("projects")

    return render(request, 'milestones/index.html', {'m_projects': mprojects, 'pageTitle': u'Цели', 'activeMenuItem': activeMenuItem})
