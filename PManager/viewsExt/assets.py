# -*- coding:utf-8 -*-
__author__ = 'Rayleigh'

from django.http import HttpResponseForbidden, HttpResponse
from PManager.services.access import assets_access


def protected_file(request):
    if not assets_access(request.user, request.GET.get('uri', None)):
        return HttpResponseForbidden()
    response = HttpResponse()
    response['X-Accel-Redirect'] = request.GET.get('uri', None)
    response['Content-Type'] = ''
    return response