# -*- coding:utf-8 -*-
__author__ = 'Rayleigh'
from django.template import Library
from tracker import settings

register = Library()


@register.filter(name='get_settings')
def get_settings(value):
    accessible_values = (
        'GITOLITE_ACCESS_URL',
        'SOCKET_SERVER_ADDRESS',
        'STATIC_URL',
        'SERVER_ROOT_URL',
        'HTTP_ROOT_URL',
        'SITE_EMAIL',
        'ADMIN_EMAIL',
        'INFO_EMAIL'
    )
    if hasattr(settings, value) and value in accessible_values:
        return settings[value]
    return ""
