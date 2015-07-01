__author__ = 'gvammer'
from django.shortcuts import HttpResponse
from PManager.models import PM_Project
from git import *
from PManager.classes.git.warden import Warden
from PManager.classes.sniffer.js_sniffer import JSSniffer
from PManager.classes.sniffer.php_sniffer import PHPSniffer

def get_errors(request):
    project_id = request.POST.get('project', False)
    path = request.POST.get('path', False)
    user = request.user
    if user.is_authenticated() and path and project_id:
        project = PM_Project.objects.get(id=int(project_id))
        if project:
            warden = Warden(user, project, is_loaded=True)
            _repo = Repo(warden.repo_path)
            ext = path.split('.').pop()

            if ext == 'php' or ext == 'js':
                r = _repo.git.show('master:' + path[1:])
                filename = 'tracker/sniffer_files/tmp' + str(user.id)
                f = open(filename, 'w')
                f.write(r)
                f.close()

                a = ''
                if ext == 'php':
                    a = JSSniffer.sniff(filename)
                elif ext == 'js':
                    a = PHPSniffer.sniff(filename)

                sOut = ''
                for s in a:
                    sOut += s

                os.remove(filename)

                return HttpResponse(sOut)

    return HttpResponse('User is not authenticated or not found required params')