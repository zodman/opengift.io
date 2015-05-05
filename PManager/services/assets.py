# -*- coding:utf-8 -*-
__author__ = 'Rayleigh'

from PManager.services.access import project_access


def assets_access_control(user, uri):
    try:
        (project_id, file_path) = uri.replace('/static/upload/projects/', '').split('/', 1)
        access = project_access(int(project_id), user.id)
        return access
    except (ValueError, AttributeError):
        return True


def assets_get_url(url):
    try:
        protected_url = '/protected' + url
        return protected_url
    except (ValueError, AttributeError):
        return url
