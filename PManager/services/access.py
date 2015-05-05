# -*- coding:utf-8 -*-
__author__ = 'Rayleigh'

from PManager.models import PM_ProjectRoles


def project_access(project_id, user_id):
    try:
        qs = PM_ProjectRoles.objects.filter(user__id=user_id, project__id=project_id)
        if qs.count() > 0:
            return True
        else:
            return False
    except PM_ProjectRoles.DoesNotExist:
        return False