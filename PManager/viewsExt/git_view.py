# -*- coding:utf-8 -*-
__author__ = 'Tonakai'

from django.shortcuts import HttpResponse, render
from PManager.models import PM_Task_Message
from django.http import Http404
from tracker import settings

class GitView(object):
    @classmethod
    def show_commit(cls, request):
        try:
            _message = int(request.GET.get('message_id'))
            _message = PM_Task_Message.objects.get(id=_message)
        except PM_Task_Message.DoesNotExist:
            raise Http404
        except ValueError:
            raise Http404
        if not _message.canView(request.user):
            raise Http404
        return cls.__diff_render(request, _message)

    @classmethod
    def __diff_render(cls, request, message):
        if settings.USE_GIT_MODULE:
            from PManager.classes.git.warden import Warden
            diff = Warden.get_diff(message)
            if not diff:
                raise Http404
        else:
            diff = None
        return render(request, 'details/git_diff.html', {"diff": diff, "author": message.author.id, "project": message.project.id})