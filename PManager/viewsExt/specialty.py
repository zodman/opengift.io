__author__ = 'Alwx'
from django.http import HttpResponse
from PManager.models import PM_Skills
from django.contrib.auth.models import User


def skills_ajax(request):
    response_text = ''
    if request.POST.get('skill_search', False):
        response_text = search_skills(request)
    return HttpResponse(response_text)

def search_skills(request):
    return True
