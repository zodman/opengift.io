__author__ = 'Gvammer'
from django.shortcuts import HttpResponse
from PManager.models import PM_User
from django.template import loader, RequestContext
from PManager.services.docker import blockchain_user_register_request

def blockchainMain(request):
    c = RequestContext(request, {})

    return HttpResponse(loader.get_template('blockchain/index.html').render(c))

def blockchainAjax(request):
    result = blockchain_user_register_request(request.user.username)
    if result.find('Error') > -1:
        res = "\n\n".split(result)
        profile = request.user.get_profile()
        profile.blockchain_key = res[0]
        profile.blockchain_cert = res[1]
        profile.save()

    return HttpResponse(result)