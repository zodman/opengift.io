# -*- coding:utf-8 -*-
__author__ = 'gvammer'
from django.shortcuts import HttpResponse
from PManager.models import PM_Project
from git import *
from django.contrib.auth.models import User
import os
from tracker import settings

def get_errors(request):
    if not settings.USE_GIT_MODULE:
        return HttpResponse('No git module installed')
    from PManager.classes.sniffer.js_sniffer import JSSniffer
    from PManager.classes.sniffer.php_sniffer import PHPSniffer
    from PManager.classes.git.warden import Warden
    project_id = request.POST.get('project', False)
    path = request.POST.get('path', False)
    user = request.POST.get('user', False)
    user = User.objects.get(id=user)
    if request.user.is_authenticated() and path and project_id:
        project = PM_Project.objects.get(id=int(project_id))
        if project and request.user.get_profile().hasRole(project):
            warden = Warden(user, project, is_loaded=True)
            _repo = Repo(warden.repo_path)
            ext = path.split('.').pop()

            if ext == 'php' or ext == 'js':
                try:
                    r = _repo.git.show('master:' + path[1:])
                except GitCommandError as e:
                    return HttpResponse(e)

                filename = 'tracker/sniffer_files/tmp' + str(user.id)
                f = open(filename, 'w')
                f.write(r)
                f.close()

                a = []
                if ext == 'php':
                    a = PHPSniffer.sniff(filename)
                elif ext == 'js':
                    a = JSSniffer.sniff(filename)

                sOut = u'<table><tr><th>Номер строки</th><th>Тип ошибки</th><th>Текст</th></tr>'
                for s in a:
                    sOut += '<tr><td>'+s['line']+'</td><td>'+s['type']+'</td><td>'+s['comment']+'</td></tr>'
                sOut += '</table>'
                os.remove(filename)

                return HttpResponse(sOut)

    return HttpResponse('User is not authenticated or not found required params')
