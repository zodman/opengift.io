# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from PManager.classes.git.gitolite_manager import GitoliteManager
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from PManager.viewsExt.tools import emailMessage
from PManager.viewsExt.headers import initGlobals
from PManager.models.users import PM_User
from tracker.settings import USE_GIT_MODULE
from PManager.viewsExt.tasks import TaskWidgetManager
from django.db.models import Q
import json

class userHandlers:
    @staticmethod
    def getMyTeam(request):
        widgetManager = TaskWidgetManager()
        resps = widgetManager.getResponsibleList(request.user, None)
        if request.POST.get('q'):
            q = request.POST.get('q')
            resps = resps.filter(Q(Q(first_name__contains=q) | Q(last_name__contains=q)))

        aResps = []
        for resp in resps:
            p = resp.get_profile()
            respDict = {
                'first_name': resp.first_name,
                'last_name': resp.last_name,
                'avatar': p.avatarSrc,
                'rel': p.avatarParams,
                'id': resp.id
            }
            histasksQty = resp.todo.filter(active=True, closed=False).count()
            respDict['openTasksQty'] = histasksQty
            aResps.append(respDict)

        return HttpResponse(json.dumps(aResps))

    @staticmethod
    def setUserOptions(request):
        action = request.POST['action']
        if not request.user.is_authenticated():
            return HttpResponse('')

        curUser = request.user

        response = u''
        if action == 'setRole':
            userId = request.POST['user']
            projectId = int(request.REQUEST.get('project', 0))
            if projectId:
                managedProjects = curUser.get_profile().managedProjects
                for p in managedProjects:
                    if projectId == p.id:
                        roleCode = request.POST.get('role', None)
                        set = int(request.POST.get('set', 0))
                        user = User.objects.get(pk=userId)
                        prof = user.get_profile()

                        if set:
                            prof.setRole(roleCode, p)
                        else:
                            prof.deleteRole(roleCode, p)

                return HttpResponse('ok')
        elif action == 'inviteUser':
            email = request.POST.get('email', None)
            roles = request.POST.getlist('roles[]', [])

            if email:
                if not emailMessage.validateEmail(email):
                    return HttpResponse(u'Email введен неверно')
                if not roles:
                    return HttpResponse(u'Не введено ни одной роли')

                headers = initGlobals(request)
                p = headers['CURRENT_PROJECT']
                if request.user.get_profile().isManager(p):
                    if p:
                        user = PM_User.getOrCreateByEmail(email, p, roles.pop())
                        if USE_GIT_MODULE:
                            GitoliteManager.regenerate_access(p)
                        for role in roles:
                            user.get_profile().setRole(p, role)

            return HttpResponse('ok')
        elif action == 'getUsers':
            return userHandlers.getMyTeam(request)
class usersActions:
    def set_user_roles(self):
        pass