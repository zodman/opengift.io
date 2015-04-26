# -*- coding:utf-8 -*-
__author__ = 'rayleigh'
import json
from django.http import HttpResponse, Http404
from PManager.services import get_draft_by_slug
from django.template import loader, RequestContext


def taskdraft_detail(request, draft_slug):
    draft = get_draft_by_slug(draft_slug, request.user)
    if not draft:
        raise Http404
    if request.method == 'GET':
        return __show(request, draft)
    elif request.method == 'POST':
        req_method = request.POST.get('_method', 'POST')
        if req_method == 'DELETE':
            return __delete(request, draft)
        elif req_method == 'PUT':
            raise Http404
        else:
            raise Http404
    raise Http404


def __show(request, draft):
    users = draft.users.all()
    tasks = draft.tasks.select_related('resp', 'project', 'milestone', 'parentTask__id', 'author', 'status').all()
    context = RequestContext(request, {
        'users': users,
        'tasks': tasks,
        'draft': draft
    })
    template = loader.get_template('details/taskdraft.html')
    return HttpResponse(template.render(context))


def __delete(request, draft):
    if draft.author.id != request.user.id:
        return HttpResponse(json.dumps({'result': 'error'}))
    draft.deleted = True
    draft.save()
    return HttpResponse(json.dumps({'result': 'ok'}))
