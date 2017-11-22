__author__ = 'Gvammer'
from django.shortcuts import HttpResponse
from PManager.models import PM_User
from django.template import loader, RequestContext
from PManager.services.docker import blockchain_user_register_request

def blockchainMain(request):
    c = RequestContext(request, {})

    return HttpResponse(loader.get_template('blockchain/index.html').render(c))

def blockchainAjax(request):
    return HttpResponse(blockchain_user_register_request(request.user.username))