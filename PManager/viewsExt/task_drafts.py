# -*- coding:utf-8 -*-
from PManager.viewsExt.tools import templateTools

__author__ = 'rayleigh'
import json
from django.http import HttpResponse, Http404
from PManager.services import get_draft_by_slug
from django.template import loader, RequestContext
from PManager.services.task_list import tasks_to_tuple, task_list_prepare

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
    add_tasks = dict()
    user = request.user.get_profile()
    for task in tasks:
        add_tasks[task.id] = {
            'url': task.url,
            'project': {
                'name': task.project.name
            },
            'canSetPlanTime': task.canPMUserSetPlanTime(user),
            'status': task.status.code if task.status else '',
            'last_message': {'text': task.text},
            'resp': [
                {'id': task.resp.id,
                 'name': task.resp.first_name + ' ' + task.resp.last_name if task.resp.first_name else task.resp.username} if task.resp else {}
            ]
        }
    tasks = tasks_to_tuple(tasks)
    tasks = task_list_prepare(tasks, add_tasks)

    context = RequestContext(request, {
        'users': users,
        'tasks': tasks,
        'draft': draft,
        'tasks_template': templateTools.get_task_template('draft_task')
    })
    template = loader.get_template('details/taskdraft.html')
    return HttpResponse(template.render(context))


def __delete(request, draft):
    if draft.author.id != request.user.id:
        return HttpResponse(json.dumps({'result': 'error'}))
    draft.deleted = True
    draft.save()
    return HttpResponse(json.dumps({'result': 'ok'}))
