# -*- coding:utf-8 -*-
from __future__ import division

__author__ = 'Gvammer'
from PManager.models import PM_ProjectRoles, PM_Project, PM_Task, PM_Timer
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponseRedirect
from PManager.viewsExt.headers import TRACKER
from PManager.viewsExt.tasks import TaskWidgetManager
import datetime, itertools
from django.utils import timezone
def union(it1, it2):
    it1, it2 = iter(it1), iter(it2)
    for item in (item for pair in itertools.izip(it1, it2) for item in pair):
        yield item
    for it in (it1, it2):
        for item in it:
            yield item

def widget(request, headerValues, a, b):
    users = TaskWidgetManager.getUsersThatUserHaveAccess(request.user, headerValues['CURRENT_PROJECT'])
    users = users.order_by('last_name')
    projects = PM_Project.objects.filter(tracker=TRACKER, closed=False, locked=False)
    now = timezone.make_aware(datetime.datetime.now(), timezone.get_current_timezone())
    arFilter = {}
    if 'auth' in request.GET:
        if request.user.is_superuser:
            uid = int(request.GET.get('auth', 0))
            if uid:
                try:
                    user = User.objects.get(pk=uid)
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    auth.login(
                        request,
                        user
                    )
                    return HttpResponseRedirect("/")
                except User.DoesNotExist:
                    pass

    if headerValues['CURRENT_PROJECT']:
        arFilter['userRoles__in'] = PM_ProjectRoles.objects.filter(project=headerValues['CURRENT_PROJECT'])
        users = users.filter(**arFilter).distinct()
    # users = union(users, [request.user,])
    allUsersTaskQty = 0
    for user in users:
        userJoinTime = now - datetime.timedelta(days=30)
        # userJoinTime = userJoinTime.days if userJoinTime.days > 0 else 1
        # userJoinTime = 30
        taskClosedQty = PM_Task.objects.filter(closed=True, resp=user, dateClose__gte=userJoinTime, active=True).count()
        userRoles = user.userRoles.filter(project__in=projects)
        setattr(user, 'roles_in_projects', userRoles)

        profile = user.get_profile()

        if profile.avatar:
            profile.avatar = str(profile.avatar).replace('PManager', '')

        allTasksQty = user.todo.filter(active=True, closed=False).count()
        if allUsersTaskQty < allTasksQty:
            allUsersTaskQty = allTasksQty

        setattr(user, 'profile', profile)
        setattr(user, 'tasksQty', taskClosedQty)
        setattr(user, 'allTasksQtyForDivision', allTasksQty * 100)

        try:
            if user.pk:
                startedTimer = PM_Timer.objects.get(user__id=user.pk, dateEnd=None)
                setattr(user, 'bHaveAccessToStartedTask', user.get_profile().isManager(startedTimer.task.project))
                setattr(user, 'startedTask', startedTimer.task)
        except PM_Timer.DoesNotExist:
            pass

        if not user.email and user.username.find('@'):
            setattr(user, 'email', user.username)

    return {
        'users': users,
        'allTasksQty': allUsersTaskQty or 1, #exclude division by zero in template
        'currentProject': int(request.GET.get('project', 0)),
        'title': u'Список пользователей'
    }