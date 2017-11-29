__author__ = 'Gvammer'
from django.shortcuts import HttpResponse
from PManager.models import PM_User
from django.template import loader, RequestContext
class Public:
    @staticmethod
    def mainPage(request):
        c = RequestContext(request, {

        })

        return HttpResponse(loader.get_template('public/index.html').render(c))