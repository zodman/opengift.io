# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from django.shortcuts import HttpResponse, render, HttpResponseRedirect
from PManager.models import PM_Milestone, PM_Project, PM_Task
from django.template import RequestContext
from PManager.viewsExt.tools import templateTools
from PManager.viewsExt import headers
from PManager.widgets.gantt.widget import create_milestone_from_post


def releasesResponder(request, activeMenuItem=None):
    from PManager.viewsExt import headers

    headerValues = headers.initGlobals(request)
    create_milestone_from_post(request, headerValues)
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect('/')

    mprojects = []
    try:
        mprojects = [headerValues["CURRENT_PROJECT"]]
    except Exception:
        pass

    return render(request, 'releases/index.html', {'projects': mprojects, 'pageTitle': u'Релизы', 'activeMenuItem': 'releases'})