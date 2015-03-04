# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from django.shortcuts import HttpResponse, HttpResponseRedirect, get_object_or_404, render
from django.http import Http404
from django.template import loader, RequestContext
from django.contrib.auth.models import User
from PManager.models import PM_Project, PM_ProjectRoles, AccessInterface, Credit, Payment
from django import forms
from tracker.settings import USE_GIT_MODULE
import json

class InterfaceForm(forms.ModelForm):
    class Meta:
        model = AccessInterface
        fields = ["name", "address", "port", "protocol", "username", "password", "access_roles", "project"]

def projectDetail(request, project_id):
    project = get_object_or_404(PM_Project, id=project_id)
    profile = request.user.get_profile()
    if not profile.hasRole(project):
        raise Http404('Project not found')

    aMessages = {
        'client': u'Бонусы за каждый час закрытых задач списываются с клиента, у которого установлена ставка.',
        'manager': u'Менеджеры получают бонусы за каждый час закрытых задач, в которых они являются наблюдателями.',
        'employee': u'Сотрудники получают бонусы за время, потраченное ими на задачи. Бонусы за плановое время распределяются поровну.',
    }
    show = dict(manager=True)
    show['employee'] = profile.isManager(project) or profile.isEmployee(project)
    show['client'] = profile.isManager(project) or profile.isClient(project)

    aDebts = Credit.getUsersDebt([project])
    oDebts = dict()
    for x in aDebts:
        oDebts[x['user_id']] = x['sum']

    aRoles = dict()

    for role in PM_ProjectRoles.objects.filter(project=project):
        if not show[role.role.code]:
            continue

        if role.role.name not in aRoles:
            aRoles[role.role.name] = dict(role=role, users=[], text=aMessages[role.role.code])

        prof = role.user.get_profile()
        setattr(role.user, 'rate', role.rate)
        setattr(role.user, 'defaultRate', prof.sp_price + (prof.rating or 0))
        setattr(role.user, 'sum', oDebts.get(role.user.id, ''))
        setattr(role.user, 'role_id', role.id)
        aRoles[role.role.name]['users'].append(role.user)

    bCurUserIsAuthor = request.user.id == project.author.id
    if bCurUserIsAuthor:
        action = request.POST.get('action', None)
        if action:
            role_id = request.POST.get('role')
            try:
                role = PM_ProjectRoles.objects.get(pk=role_id, project=project)
                if action == 'update_payment_type':
                    type = 'real_time' if request.POST.get('value') == 'real_time' else 'plan_time'
                    role.payment_type = type
                    role.save()
                    responseObj = {'result': 'payment type updated'}
                elif action == 'update_rate':
                    rate = int(request.POST.get('value'))
                    role.rate = rate
                    role.save()
                    responseObj = {'result': 'rate updated'}
                elif action == 'send_payment':
                    sum = int(request.POST.get('sum'))
                    p = Payment(user=role.user, project=project, value=sum)
                    p.save()

                    responseObj = {'result': 'payment added'}

            except PM_ProjectRoles.DoesNotExist:
                responseObj = {'error': 'Something is wrong  :-('}

            return HttpResponse(json.dumps(responseObj))

    canDeleteInterface = profile.isManager(project)
    canDeleteProject = canDeleteInterface
    canEditProject = request.user.is_staff

    if 'archive' in request.GET and request.GET['archive'] == 'Y' and canDeleteProject:
        project.closed = True
        project.save()
        return HttpResponseRedirect('/project/'+str(project.id)+'/')

    interfaces = AccessInterface.objects.filter(project=project)
    interfaces_html = ''
    t = loader.get_template('details/interface.html')
    for interface in interfaces:
        c = RequestContext(request, {
            'interface': interface,
            'canDelete': canDeleteInterface,
            'show_git': USE_GIT_MODULE
        })

        interfaces_html += t.render(c)

    c = RequestContext(request, {
        'project': project,
        'roles': aRoles,
        'form': InterfaceForm(),
        'interfaces': interfaces_html,
        'canDelete': canDeleteProject,
        'canEdit': canEditProject,
        'bCurUserIsAuthor': bCurUserIsAuthor,
        'messages': aMessages
    })
    t = loader.get_template('details/project.html')
    return HttpResponse(t.render(c))

def addInterface(request):
    post = request.POST
    try:
        project_id = int(post['pid'])
        project = PM_Project.objects.get(id=project_id)
        if request.user.get_profile().hasRole(project):
            post['project'] = project.id
            form = InterfaceForm(data=post)
            if form.is_valid():
                instance = form.save()
                return render(request, 'details/interface.html', {
                    'interface': instance
                })
    except PM_Project.DoesNotExist:
        pass

    return HttpResponse('Invalid form')

def removeInterface(request):
    interface = get_object_or_404(AccessInterface, id=int(request.POST['id']))
    if request.user.get_profile().isManager(interface.project):
        interface.delete()

    return HttpResponse('ok')

def checkUniqRepNameResponder(request):
    if not USE_GIT_MODULE:
        return HttpResponse("OK")
    if not request.POST['repoName']:
        return HttpResponse("ERROR")
    if request.POST['repoName'] == "gitolite-admin":
        return HttpResponse("ERROR")
    proj = PM_Project.objects.filter(repository=request.POST['repoName'])
    if(proj):
        if not USE_GIT_MODULE:
            return HttpResponse("OK")
        from PManager.classes.git.gitolite_manager import GitoliteManager
        reponame = GitoliteManager.get_suggested_name(request.POST['repoName'])
        if not reponame:
                return HttpResponse("ERROR")
        else:
            return HttpResponse(reponame)
    return HttpResponse("OK")