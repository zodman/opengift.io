# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from PManager.models import PM_Task, PM_Timer, PM_Task_Message, PM_User_PlanTime, PM_ProjectRoles
import datetime, json
from PManager.viewsExt.tools import TextFilters, taskExtensions
from PManager.widgets.tasklist.widget import widget as taskList
from PManager.viewsExt.tasks import TaskWidgetManager
from PManager.viewsExt.tools import templateTools
from django.db.models import Q
from django.http import Http404

from PManager.services.mind.task_mind_core import TaskMind
from PManager.viewsExt.tools import redisSendTaskUpdate

def widget(request, headerValues, arFilter, q):
    widgetManager = TaskWidgetManager()
    cur_user = request.user
    prof = request.user.get_profile()
    task = None
    if 'id' in request.GET or 'number' in request.GET:
        if 'id' in request.GET:
            task = PM_Task.objects.filter(id=int(request.GET.get('id')), active=True).get()
        elif 'number' in request.GET and 'project' in request.GET:
            task = PM_Task.objects.filter(
                number=int(request.GET.get('number')),
                project=int(request.GET.get('project')),
                parentTask__isnull=True,
                active=True
            )[0]

        if not task:
            raise Http404(u'Задача удалена')

        if not cur_user.get_profile().hasAccess(task, 'view'):
            raise Http404(u'Нет прав для просмотра задачи')

        error = ''
        cid = int(request.GET.get('confirm', 0))
        if cid:
            try:
                message = PM_Task_Message.objects.get(pk=cid, task=task)
                planTime = PM_User_PlanTime.objects.get(task=task, user=message.author)

                #client have not enough money#
                clientProfile = None
                pref = None
                if prof.isClient(task.project):
                    clientProfile = prof
                    pref = '<h3>На вашем счету недостаточно средств для данной задачи</h3>' + \
                            '<hr>' + \
                            '<div class="border-wrapper">' + \
                            '<p>Вы можете бесплатно пригласить в систему собственных исполнителей, создав для них задачу, или пополнить счет и воспользоваться услугами любого из тысяч уже зарегистрированных пользователей.</p>' + \
                            '<hr>' + \
                            '<p><img src="/static/images/robokassa.png" class="img-responsive"></p>' + \
                            '<hr>' + \
                            '<p align="center"><a href="" class="btn  btn-large btn-success">Пополнить баланс</a>' + \
                            '</div>'
                    # pref = u'У вас недостаточно средств. Пожалуйста, пополните ваш счет.'
                else:
                    try:
                        clientRole = PM_ProjectRoles.objects.get(
                            role__code='client',
                            project=task.project,
                            user__is_staff=True
                        )
                        client = clientRole.user
                        clientProfile = client.get_profile()
                        pref = u'У клиента едостаточно средств.'
                    except PM_ProjectRoles.DoesNotExist:
                        pass

                if clientProfile:
                    if not prof.account_total or prof.account_total < prof.getBet(task.project) * planTime.time:
                        error = pref

                if not error:
                    authorProf = message.author.get_profile()

                    if not authorProf.hasRole(task.project):
                        authorProf.setRole('employee', task.project)

                    if not authorProf.isEmployee(task.project):
                        task.resp = prof.user
                    else:
                        task.resp = planTime.user

                    task.planTime = planTime.time
                    task.onPlanning = False
                    task.setStatus('revision')
                    task.save()
                    redisSendTaskUpdate({
                        'status': task.status.code,
                        'onPlanning': task.onPlanning,
                        'planTime': task.planTime,
                        'resp': [{
                            'id': task.resp.id,
                            'name': task.resp.first_name + ' ' + task.resp.last_name
                        }],
                        'viewedOnly': request.user.id,
                    })


                    task.systemMessage(
                        u'подтвердил(а) оценку в ' + str(task.planTime) +
                        u'ч. пользователя ' + planTime.user.first_name +
                        u' ' + planTime.user.last_name,
                        cur_user,
                        'CONFIRM_ESTIMATION'
                    )

                    task.sendTaskEmail('new_task', [planTime.user.email])

                    return {'redirect': task.url}
            except PM_Task_Message.DoesNotExist:
                pass
            except PM_User_PlanTime.DoesNotExist:
                pass

        setattr(task, 'text_formatted', TextFilters.getFormattedText(task.text))
        # setattr(task, 'responsibleList', task.responsible.all())
        setattr(task, 'observersList', task.observers.all())
        setattr(task, 'canSetOnPlanning', task.onPlanning or task.canEdit(cur_user))
        setattr(task, 'canSetPlanTime', task.canPMUserSetPlanTime(prof))
        setattr(task, 'canSetCritically', task.canEdit(cur_user))
        setattr(task, 'canEdit', task.canEdit(cur_user))
        setattr(task, 'canRemove', task.canPMUserRemove(prof))
        setattr(task, 'canApprove', cur_user.id == task.author.id or prof.isManager(task.project))
        setattr(task, 'canClose', task.canApprove)
        setattr(task, 'taskPlanTime', task.planTime)

        setattr(task, 'taskResp', [{'id': task.resp.id, 'name': task.resp.first_name + ' ' + task.resp.last_name if task.resp.first_name else task.resp.username} if task.resp else {}])

        allTime = task.getAllTime()
        files = taskExtensions.getFileList(task.files.all())

        if task:
            #set task readed
            if not request.user.id in [u.id for u in list(task.viewedUsers.all())]:
                task.viewedUsers.add(request.user)

            hiddenSubTasksExist = False
            arFilter = {
                'parentTask': task
            }
            subtasks = taskList(request, headerValues, {'filter': arFilter}, [], {})
            subtasks = subtasks['tasks']
            for subtask in subtasks:
                if subtask['closed']:
                    hiddenSubTasksExist = True
                    break

        users = widgetManager.getResponsibleList(request.user, headerValues['CURRENT_PROJECT'])
        dict = task.__dict__

        for field, val in dict.iteritems():
            if isinstance(val, datetime.datetime):
                setattr(task, field, val.strftime('%d.%m.%Y %H:%M'))

        messages = task.messages.order_by('dateCreate')
        # userRoles = PM_ProjectRoles.objects.filter(user=request.user, role__code='manager')
        if not request.user.is_superuser:
            messages = messages.filter(Q(hidden=False) | Q(userTo=request.user.id))

        if not prof.isManager(task.project):
            if prof.isClient(task.project):
                messages = messages.filter(hidden_from_clients=False)
            if prof.isEmployee(task.project):
                messages = messages.filter(hidden_from_employee=False)

        lamp, iMesCount = 'no-asked', messages.count()

        if iMesCount > 0 and messages[iMesCount - 1]:
            if messages[iMesCount - 1].author and messages[iMesCount - 1].author.id == cur_user.id:
                lamp = 'asked'
        arTodo = []
        for mes in messages:
            if mes.userTo and mes.userTo.id == request.user.id:
                mes.read = True
                mes.save()

            if mes.todo:
                arTodo.append({
                    'id': mes.id,
                    'text': mes.text,
                    'checked': mes.todo_checked
                })

            ob = {
                'canEdit': mes.canEdit(request.user),
                'canDelete': mes.canDelete(request.user),
            }
            if cur_user.get_profile().isManager(task.project):
                ob.update({
                    'hidden_from_clients': mes.hidden_from_clients,
                    'hidden_from_employee': mes.hidden_from_employee
                })
            setattr(mes, 'json', json.dumps(mes.getJson(ob, request.user)))

        try:
            startedTimer = PM_Timer.objects.get(task=task, dateEnd__isnull=True)
        except PM_Timer.DoesNotExist:
            startedTimer = None

        setattr(task, 'todo', arTodo)
        templates = templateTools.getMessageTemplates()
        taskTemplate = templateTools.getDefaultTaskTemplate()

        brain = TaskMind()
        return {
            'title': task.name,
            'task': task,
            'startedTimerExist': startedTimer != None,
            'startedTimerUserId': startedTimer.user.id if startedTimer else None,
            'project': task.project,
            'is_employee': cur_user.get_profile().isEmployee(task.project),
            'is_manager': cur_user.get_profile().isManager(task.project),
            'user_roles': cur_user.get_profile().getRoles(task.project),
            'files': files,
            'time': allTime,
            'subtasks': subtasks,
            'taskTemplate': taskTemplate,
            'users': users,
            'messages': messages,
            'lamp': lamp,
            'hiddenSubTasksExist': hiddenSubTasksExist,
            'templates': templates,
            'resultTime': task.planTime if task.planTime else int(round(brain.check(task))),
            'error': error
            # 'dataSet': len(arParams),
            # 'similarSet': len(tasksSimilar),
            # 'params': arParams
        }