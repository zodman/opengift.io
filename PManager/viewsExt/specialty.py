__author__ = 'Alwx'
from django.http import HttpResponse
from PManager.models import Specialty
from django.contrib.auth.models import User
import json


def specialty_ajax(request):
    response_text = ''
    if request.POST.get('specialty_search', False):
        response_text = search_specialty(request)
    return HttpResponse(response_text)

def search_specialty(request):
    search_text = request.get('specialty_search')
    userId = request.get('user')
    user = User.objects.get(pk=userId)
    profile = user.get_profile()
    profile_specialties = profile.specialties.values_list('name', flat=True)
    specialties = Specialty.objects.filter(search_text).exclude(profile_specialties)
    response_text = json.dumps({'specialties': specialties, 'count': len(specialties)})
    return response_text
