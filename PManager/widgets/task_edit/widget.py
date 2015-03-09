# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from PManager.viewsExt.tools import templateTools
from PManager.models import PM_Task, PM_Project, ObjectTags, PM_User, PM_Task_Status
import time, datetime
from django.contrib.auth.models import User
from django.db.models import Count
from PManager.viewsExt.tasks import TaskWidgetManager
from PManager.widgets.tasklist.widget import get_user_tag_sums, get_task_tag_rel_array
import json
from django.http import HttpResponse


def widget(request, headerValues, ar, qargs):
    widgetManager = TaskWidgetManager()
    post = request.POST
    deadline = post.get('deadline', time.strftime('%d.%m.%Y'))

    deadline = templateTools.dateTime.convertToDateTime(deadline)
    name = post.get('name', False)
    status = post.get('status', False)
    if status:
        status = PM_Task_Status.objects.get(code=status)

    if request.GET.get('id', False):
        task = PM_Task.objects.get(id=int(request.GET.get('id', False)))
    else:
        task = False

    userTagSums = {}

    if name:
        planTime = post.get('planTime', 0)
        if planTime:
            planTime = planTime.replace(',', '.')

        arSaveFields = {
            'name': name,
            'text': post.get('description', ''),
            'repeatEvery': post.get('repeatEvery', 0),
            'deadline': deadline,
            'critically': float(post.get('critically', 0)) if post.get('critically', 0) else 0.5,
            'hardness': float(post.get('hardness', 0)) if post.get('hardness', 0) else 0.5,
            'project_knowledge': float(post.get('project_knowledge', 0)) if post.get('project_knowledge', 0) else 0.5,
            'reconcilement': float(post.get('reconcilement', 0)) if post.get('reconcilement', 0) else 0.5,
            'planTime': float(planTime),
            'status': status if status else task.status
        }
        if task:
            for k, val in arSaveFields.iteritems(): setattr(task, k, val)
        else:
            arSaveFields['author'] = request.user
            task = PM_Task(**arSaveFields)

        respId = post.get('resp', '')

        if str(respId).find('@') > -1:
            oUserProfile = PM_User.getOrCreateByEmail(respId, task.project, 'employee')
            respId = oUserProfile.id
        if respId:
            task.resp = User.objects.get(pk=int(respId))
            arSaveFields['resp'] = task.resp

        task.save()
        aObservers = post.getlist('observers')
        for (counter, observer) in enumerate(aObservers):
            if observer.find('@') > -1:
                oUserProfile = PM_User.getOrCreateByEmail(observer, task.project, 'employee')
                aObservers[counter] = oUserProfile.id

        task.observers.clear()
        task.observers.add(*aObservers)

        task.saveTaskTags()

        arEmail = task.getUsersEmail([request.user.id])
        task.sendTaskEmail('task_changed', arEmail, 'Задача изменена')

        backurl = request.GET.get('backurl', None)
        if backurl:
            return {'redirect': backurl}

    elif request.GET.get('id', False):
        arSaveFields = task
        if arSaveFields:
            tagsRelations = []
            aSimilarTasks = []

            resp = arSaveFields.resp
            observers = arSaveFields.observers.all()
            tags = arSaveFields.tags.all()
            arSaveFields = arSaveFields.__dict__
            tagsRelations = ObjectTags.objects.filter(tag__in=tags.values('tag')).annotate(
                dcount=Count('object_id')) if tags else []


            if tagsRelations:
                aTasksFromRelations = []
                for rel in tagsRelations:
                    aTasksFromRelations.append(rel.object_id)
                aSimilarTasks = PM_Task.objects.filter(pk__in=aTasksFromRelations, project=task.project).exclude(
                    id=task.id)[:4]

            aUsersHaveAccess = widgetManager.getResponsibleList(request.user, None).values_list('id', flat=True)
            currentRecommendedUser, userTagSums = get_user_tag_sums(get_task_tag_rel_array(task), None, aUsersHaveAccess)

            arSaveFields.update({
                'tags': tags,
                'resp': resp,
                'observers': observers,
                'critically': arSaveFields.get('critically', 0.5),
                'hardness': arSaveFields.get('hardness', 0.5),
                'project_knowledge': arSaveFields.get('project_knowledge', 0.5),
                'reconcilement': arSaveFields.get('reconcilement', 0.5),
                'similarTasks': aSimilarTasks,
                'tagsRelations': tagsRelations,
                'files': task.files.all(),
                'status': status if status else task.status
            })

    else:
        arSaveFields = {}

    users = widgetManager.getResponsibleList(request.user, headerValues['CURRENT_PROJECT'])

    for field, val in arSaveFields.iteritems():
        if isinstance(val, datetime.datetime):
            arSaveFields[field] = val.strftime('%d.%m.%Y %H:%M')

    return {
        'id': request.GET.get('id', False),
        'post': arSaveFields,
        'project': task.project if task and task.project else headerValues['CURRENT_PROJECT'],
        'users': users,
        'recommendedUsers': [i for i, c in userTagSums.iteritems()],
    }