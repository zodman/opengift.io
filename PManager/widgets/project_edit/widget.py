# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from PManager.models import PM_Project
from django.contrib.auth.models import User
from django import forms
from django.template import RequestContext
from django.core.context_processors import csrf
from PManager.classes.git import *
from PManager.classes.git.gitolite_manager import GitoliteManager
import json

class ProjectForm(forms.ModelForm):
    class Meta:
        model = PM_Project
        fields = ["name", "description", "image", "author", "tracker", "closed", "repository"]

def widget(request, headerValues, ar, qargs):
    if request.user.is_staff:
        SET_USER_ROLE = 'manager'
        c = RequestContext(request, processors=[csrf])
        post = request.POST
        get = request.GET
        projectData = {}
        pform = {}

        if 'id' in get:
            try:
                projectData = PM_Project.objects.get(id=int(get['id']))
                pform = ProjectForm(instance=projectData)
            except PM_Project.DoesNotExist:
                pass
        else:
            pform = ProjectForm(data=post) # A form bound to the POST data
            projectData = post

        if request.method == 'POST':
            post.update({'author': request.user.id})
            post.update({'tracker': 1})
            pform = ProjectForm(
                instance=projectData if hasattr(projectData, 'id') else None,
                data=post,
                files=request.FILES
            )


            # pform.data = post
            # pform.files = request.FILES
            if pform.is_valid():
                instance = pform.save()

                settings = {}
                for k, v in request.POST.iteritems():
                    if k.find('settings_') > -1:
                        k = k.replace('settings_', '')
                        settings[k] = v

                instance.setSettings(settings)
                instance.save()

                if not hasattr(projectData, 'id'):
                    request.user.get_profile().setRole(SET_USER_ROLE, instance)
                    GitoliteManager.add_repo(instance, request.user)
                    return {'redirect': request.get_full_path() + '?id=' + str(instance.id)}
                    
                return {'redirect': request.get_full_path()}
            else:
                pass

        return {
            'projectData': projectData,
            'form': pform,
            'settings': projectData.getSettings() if projectData and
                            hasattr(projectData, 'settings') and
                            projectData.settings else {}
        }