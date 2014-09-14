__author__ = 'Gvammer'
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User

class userHandlers:
    @staticmethod
    def setUserOptions(request):
        action = request.POST['action']
        userId = request.POST['user']

        curUser = request.user

        response = u''
        if action == 'setRole':
            projectId = int(request.REQUEST.get('project', 0))
            if projectId:
                managedProjects = curUser.get_profile().managedProjects
                for p in managedProjects:
                    if projectId == p.id:
                        roleCode = request.POST.get('role', None)
                        set = request.POST.get('set', None)
                        user = User.objects.get(pk=userId)
                        prof = user.get_profile()

                        if set:
                            prof.setRole(roleCode, p)
                        else:
                            prof.deleteRole(roleCode, p)

        return HttpResponse('ok')

class usersActions:
    def set_user_roles(self):
        pass