# -*- coding:utf-8 -*-
__author__ = 'Rayleigh'
from django.template import Library
from tracker import settings

register = Library()


@register.simple_tag(name='get_settings')
def get_settings(setting_name):
    accessible_values = (
        'GITOLITE_ACCESS_URL',
        'SOCKET_SERVER_ADDRESS',
        'STATIC_URL',
        'SERVER_ROOT_URL',
        'HTTP_ROOT_URL',
        'SITE_EMAIL',
        'ADMIN_EMAIL',
        'INFO_EMAIL',
	'SERVER_IP'
    )
    if hasattr(settings, setting_name) and setting_name in accessible_values:
        return getattr(settings, setting_name)
    return ""
