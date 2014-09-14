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
        'is_detail_page': 'detail' in currentPath
    }
    if request.user.is_authenticated():
        result['projects'] = request.user.get_profile().getProjects().order_by('name')

    return result