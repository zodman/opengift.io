# -*- coding:utf-8 -*-
__author__ = 'Rayleigh'

from django.http import HttpResponseForbidden, HttpResponse
from PManager.services.assets import assets_access_control


def protected_file(request):
    if not assets_access_control(request.user, request.GET.get('uri', None)):
        return HttpResponseForbidden()
    response = HttpResponse()
    response['X-Accel-Redirect'] = request.GET.get('uri')
    response['Content-Type'] = ''
    return response