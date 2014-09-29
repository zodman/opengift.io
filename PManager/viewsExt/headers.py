# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from PManager.models import PM_Tracker, PM_Project
from PManager.viewsExt.forms import WhoAreYou
from django.contrib.auth import logout

TRACKER = PM_Tracker.objects.get(pk=1)


#SET_COOKIE - куки, которые необходимо поставить
#CURRENT_PROJECT - текущий выбранный проект в трекере
def initGlobals(request):
    SET_COOKIE = {}

    if request.user.is_authenticated():
        myProjects = request.user.get_profile().getProjects().values('id')
        projects = []
        for project in myProjects:
            projects.append(project['id'])
    else:
        projects = []

    if 'project' in request.REQUEST:
        try:
            CURRENT_PROJECT = PM_Project.objects.get(closed=False, id=int(request.REQUEST.get('project', '-1')))
            if CURRENT_PROJECT.id in projects:
                SET_COOKIE["CURRENT_PROJECT"] = CURRENT_PROJECT.id
                request.COOKIES["CURRENT_PROJECT"] = CURRENT_PROJECT.id
        except PM_Project.DoesNotExist:
            CURRENT_PROJECT = 0

        SET_COOKIE["CURRENT_PROJECT"] = CURRENT_PROJECT.id if CURRENT_PROJECT else 0
        request.COOKIES["CURRENT_PROJECT"] = SET_COOKIE["CURRENT_PROJECT"]

    else:
        CURRENT_PROJECT = request.COOKIES.get("CURRENT_PROJECT", 0)
        if CURRENT_PROJECT:
            try:
                if int(CURRENT_PROJECT) in projects:
                    CURRENT_PROJECT = PM_Project.objects.get(pk=int(CURRENT_PROJECT))
                elif projects:
                    SET_COOKIE["CURRENT_PROJECT"] = 0
                    CURRENT_PROJECT = 0
            except PM_Project.DoesNotExist:
                CURRENT_PROJECT = 0
            except ValueError:
                CURRENT_PROJECT = 0

    # if not CURRENT_PROJECT:
    #     CURRENT_PROJECT = PM_Project.objects.filter(tracker=TRACKER, pk__in=projects)
    #     if CURRENT_PROJECT:
    #         CURRENT_PROJECT = CURRENT_PROJECT[0]
    #         SET_COOKIE["CURRENT_PROJECT"] = CURRENT_PROJECT.id

    redirect = False

    if request.method == 'POST':
        form = WhoAreYou(request.POST)

        if form.is_valid():
            currentUser = request.user
            currentUser.first_name = form.cleaned_data['name']
            currentUser.last_name = form.cleaned_data['last_name']
            currentUser.save()

            try:
                project = PM_Project.objects.get(author=currentUser)
                if form.cleaned_data['sitename']:
                    project.name = form.cleaned_data['sitename']
                    project.save()

                redirect = "/?project="+str(project.id)
            except PM_Project.DoesNotExist:
                redirect = "/"

        WhoAreYouForm = False

    elif request.user.is_authenticated() and not request.user.last_name:
        WhoAreYouForm = WhoAreYou()
    else:
        WhoAreYouForm = False

    if 'logout' in request.GET and request.user.is_authenticated():
        if request.GET['logout'] == 'Y':
            logout(request)
            redirect = "/"

    return {
        'SET_COOKIE': SET_COOKIE,
        'CURRENT_PROJECT': CURRENT_PROJECT,
        'FIRST_STEP_FORM': WhoAreYouForm,
        'REDIRECT': redirect,
        'COOKIES': request.COOKIES
    }