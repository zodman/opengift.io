# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from PManager.models import PM_Task, PM_Timer, PM_Task_Message, PM_User_PlanTime, PM_ProjectRoles
import datetime, json
from PManager.viewsExt.tools import TextFilters, taskExtensions
from PManager.widgets.tasklist.widget import widget as taskList
from PManager.viewsExt.tasks import TaskWidgetManager
from PManager.viewsExt.tools import templateTools
from django.db.models import Q

from PManager.services.mind.task_mind_core import TaskMind


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
            raise Exception(u'Задача удалена')

        if not cur_user.get_profile().hasAccess(task, 'view'):
            raise Exception(u'Нет прав для просмотра задачи')

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
                    pref = '<h3>На вашем счету недостаточно средств для пользования данной услугой</h3>' + \
                            '<hr>' + \
                            'Необходимо ' + str(clientProfile.getBet(task.project) * task.planTime) + 'sp' + \
                            '<div class="border-wrapper">'+ \
                            '<p>Вы можете бесплатно пригласить в систему собственных исполнителей, создав для них задачу или пополнить счет и воспользоваться услугами любого из тысяч уже зарегистрированных пользователей.</p>' + \
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
                    if clientProfile.account_total < clientProfile.getBet(task.project) * task.planTime:
                        error = pref

                if not error:
                    authorProf = message.author.get_profile()
                    if not authorProf.isEmployee(task.project):
                        if not prof.hasRole(task.project):
                            prof.setRole('employee', task.project)

                        task.resp = prof.user
                    else:
                        if not authorProf.hasRole(task.project):
                            authorProf.setRole('employee', task.project)

                        task.resp = planTime.user

                    task.planTime = planTime.time
                    task.onPlanning = False
                    task.setStatus('revision')
                    task.save()

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
        if not prof.isManager(task.project):
            messages = messages.filter(Q(hidden=False) | Q(userTo=request.user.id))
            if prof.isClient(task.project):
                messages = messages.filter(hidden_from_clients=False)
            if prof.isEmployee(task.project):
                messages = messages.filter(hidden_from_employee=False)

        lamp, iMesCount = 'no-asked', messages.count()

        if iMesCount > 0 and messages[iMesCount - 1]:
            if messages[iMesCount - 1].author and messages[iMesCount - 1].author.id == cur_user.id:
                lamp = 'asked'

        for mes in messages:
            if mes.userTo and mes.userTo.id == request.user.id:
                mes.read = True
                mes.save()
                
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

        templates = templateTools.getMessageTemplates()
        taskTemplate = templateTools.getDefaultTaskTemplate()

        #test
        # resultTimeIndex = []
        # resultTimeIndex1 = []
        # resultTimeIndex2 = []
        # arParams = []
        # if not task.closed and not task.planTime:
        #     tasksSimilar = PM_Task.getSimilar((task.name + task.text), task.project)
        #
        #     uids = []
        #     maxTagsQty, maxSimilarTagsQty, maxTime = 0, 0, 0
        #     maxTimeTaskid = 0
        #     arFigure = []
        #     for taskSimilar in tasksSimilar:
        #         if taskSimilar.closed:
        #             uid = task.responsible.all()[0].id if task.responsible.all() else 0
        #             if uid not in uids:
        #                 uids.append(uid)
        #
        #             objP = {
        #                 'time': taskSimilar.getAllTime(),
        #                 'similarQty': taskSimilar.tagSimilarCount,
        #                 'allTagsQty': taskSimilar.tags.count(),
        #                 'critically': taskSimilar.critically,
        #                 'userId': uid
        #             }
        #
        #             if int(objP['time']) == 0: objP['time'] = 60 * 5
        #
        #             arFigure.append(objP)
        #
        #             if maxTagsQty < objP['allTagsQty']:
        #                 maxTagsQty = objP['allTagsQty']
        #
        #             if maxSimilarTagsQty < objP['similarQty']:
        #                 maxSimilarTagsQty = objP['similarQty']
        #
        #             if maxTime < objP['time']:
        #                 maxTime = objP['time']
        #
        #             arParams.append(objP)
        #
        #
        #     if arParams:
        #         for params in arParams:
        #             params['time'] = round(float(params['time']) / float(maxTime), 2)
        #             params['similarQty'] = round(float(params['similarQty']) / float(maxSimilarTagsQty), 2)
        #             params['allTagsQty'] = round(float(params['allTagsQty']) / float(maxTagsQty), 2)
        #             params['userId'] = round(float(uids.index(params['userId'])) / float(len(uids)), 2)
        #
        #         net = buildNetwork(4, 6, 1, hiddenclass=TanhLayer)
        #         ds = SupervisedDataSet(4, 1)
        #
        #         for params in arParams:
        #             ds.addSample((
        #                              params['similarQty'],
        #                              params['allTagsQty'],
        #                              params['userId'],
        #                              params['critically']
        #                          ), (params['time'],))
        #         trainer = BackpropTrainer(net, ds)
        #         for i in range(100):
        #             trainer.train()
        #
        #         userInd = uids.index(task.responsibleList[0].id) \
        #             if task.responsibleList and task.responsibleList[0].id in uids \
        #             else len(uids)
        #
        #         resultTimeIndex = net.activate([
        #             1,
        #             round(float(task.tags.count()) / float(maxTagsQty)),
        #             round(float(userInd) / float(len(uids))),
        #             task.critically
        #         ])
        #         resultTimeIndex1 = net.activate([
        #             1,
        #             round(float(task.tags.count()) / float(maxTagsQty)),
        #             round(float(userInd) / float(len(uids))),
        #             task.critically
        #         ])
        #         resultTimeIndex2 = net.activate([
        #             1,
        #             round(float(task.tags.count()) / float(maxTagsQty)),
        #             round(float(userInd) / float(len(uids))),
        #             task.critically
        #         ])
        #/test

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