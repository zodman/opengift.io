__author__ = 'Gvammer'
from PManager.viewsExt import headers
import urllib


def get_current_path(request):
    currentPath = request.get_full_path()
    return {
        'current_path': currentPath,
        'backurl': urllib.quote(currentPath)
    }


def get_head_variables(request):
    currentPath = request.get_full_path()
    result = {
        'is_wiki': 'Y' if currentPath.find('wiki/') > -1 else 'N',
        'main': headers.initGlobals(request),
        'user': request.user,
        'is_admin': request.user.is_superuser,
        'is_staff': request.user.is_staff,
        'is_detail_page': 'detail' in currentPath,
        'referrer': request.GET.get('r', None)
    }

    if request.user.is_authenticated():
        result['account_total'] = request.user.get_profile().account_total
        projects = request.user.get_profile().getProjects(only_managed=False, locked=True).order_by('name')
        result['projects'] = []
        for project in projects:
            tasksQty = 0
            if request.user.get_profile().isManager(project):
                tasksQty = project.projectTasks.filter(active=True, closed=False).count()
            elif request.user.get_profile().isEmployee(project):
                tasksQty = project.projectTasks.filter(active=True, closed=False, resp=request.user).count()
            setattr(project, 'tasksQty', tasksQty)
            result['projects'].append(project)

    return result