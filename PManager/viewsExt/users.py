# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from PManager.classes.git.gitolite_manager import GitoliteManager
from django.shortcuts import HttpResponse, render
from django.template import loader, RequestContext
from django.contrib.auth.models import User
from PManager.viewsExt.tools import emailMessage
from PManager.viewsExt.headers import initGlobals
from PManager.models.users import PM_User, PM_Skills
from tracker.settings import USE_GIT_MODULE
from PManager.viewsExt.tasks import TaskWidgetManager
from django.db.models import Q
from PManager.viewsExt import headers
import json

class userHandlers:
    @staticmethod
    def getResponsibleMenu(request):
        headerValues = headers.initGlobals(request)
        widget_manager = TaskWidgetManager()
        draft_id = request.GET.get('draft_id', None)
        if draft_id:
            from PManager.services.task_drafts import get_draft_by_id
            draft = get_draft_by_id(draft_id, request.user)
            if draft:
                users = draft.users.exclude(id=draft.author_id)
            else:
                users = dict()
        else:
            users = widget_manager.getResponsibleList(request.user, headerValues['CURRENT_PROJECT'])
        c = RequestContext(request, {
            'users': users
            })
        t = loader.get_template('helpers/responsible_menu.html')
        return HttpResponse(t.render(c))

    @staticmethod
    def getMyTeam(request):
        widgetManager = TaskWidgetManager()
        resps = widgetManager.getResponsibleList(request.user, None)
        if request.POST.get('q'):
            q = request.POST.get('q')
            resps = resps.filter(Q(Q(first_name__icontains=q) | Q(last_name__icontains=q)))

        aResps = []
        for resp in resps:
            p = resp.get_profile()
            respDict = {
                'first_name': resp.first_name,
                'last_name': resp.last_name,
                'rel': p.avatar_rel,
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
            projectId = int(request.REQUEST.get('roleProject', 0))
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

        elif action == 'setSkill':
            userId = request.POST['user']
            skill = request.POST['skill']
            user = User.objects.get(pk=userId)
            if user == curUser or curUser.is_superuser:
                try:
                    skill = PM_Skills.objects.filter(name=skill)
                except PM_Skills.DoesNotExist:
                    skill = PM_Skills(name=skill)
                prof = user.get_profile()
                prof.skills.add(skill)
                prof.save()
                return HttpResponse('skill saved')


class usersActions:
    def set_user_roles(self):
        pass