__author__ = 'Gvammer'
from django.shortcuts import HttpResponse, HttpResponseRedirect, get_object_or_404, render
from django.http import Http404
from django.template import loader, RequestContext
from django.contrib.auth.models import User
from PManager.models import PM_Project, PM_ProjectRoles, AccessInterface
from django import forms

class InterfaceForm(forms.ModelForm):
    class Meta:
        model = AccessInterface
        fields = ["name", "address", "port", "protocol", "username", "password", "access_roles", "project"]

def projectDetail(request, project_id):
    project = get_object_or_404(PM_Project, id=project_id)
    profile = request.user.get_profile()
    if not profile.hasRole(project):
        raise Http404('Project not found')
    show = {
        'manager': True
    }
    show['employee'] = profile.isManager(project) or profile.isEmployee(project)
    show['client'] = profile.isManager(project) or profile.isClient(project)

    aRoles = {}
    for role in PM_ProjectRoles.objects.filter(project=project):
        if not show[role.role.code]:
            continue

        if role.role.name not in aRoles:
            aRoles[role.role.name] = []

        aRoles[role.role.name].append(role.user)

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
            'canDelete': canDeleteInterface
        })

        interfaces_html += t.render(c)

    c = RequestContext(request, {
        'project': project,
        'roles': aRoles,
        'form': InterfaceForm(),
        'interfaces': interfaces_html,
        'canDelete': canDeleteProject,
        'canEdit': canEditProject
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
    proj = PM_Project.objects.filter(repository=request.POST['repoName'])
    if(proj):
        return HttpResponse("ERROR")
    return HttpResponse("OK")