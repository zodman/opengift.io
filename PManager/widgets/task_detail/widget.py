# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from PManager.models import PM_User, PM_Task, Agreement, PM_Task_Message, PM_User_PlanTime, PM_Project_Donation
import datetime, json
from PManager.viewsExt.tools import TextFilters, taskExtensions
from PManager.widgets.tasklist.widget import widget as taskList
from PManager.viewsExt.tasks import TaskWidgetManager
from PManager.viewsExt.tools import templateTools
from django.db.models import Q
from django.http import Http404
from django.contrib.auth.models import User
from PManager.services.similar_tasks import similar_solutions

from PManager.services.mind.task_mind_core import TaskMind
from PManager.viewsExt.tools import redisSendTaskUpdate

def widget(request, headerValues, arFilter, q):
    widgetManager = TaskWidgetManager()
    cur_user = request.user


    prof = None
    if cur_user.is_authenticated():
        prof = request.user.get_profile()

    task = None
    if 'id' in request.GET or 'number' in request.GET:
        try:
            if 'id' in request.GET:
                task = PM_Task.objects.filter(id=int(request.GET.get('id')), active=True).get()
            elif 'number' in request.GET and 'project' in request.GET:
                task = PM_Task.objects.filter(
                    number=int(request.GET.get('number')),
                    project=int(request.GET.get('project')),
                    parentTask__isnull=True,
                    active=True
                )[0]
        except (PM_Task.DoesNotExist, ValueError, IndexError):
            task = None

        if not task:
            raise Http404(u'Задача удалена')

        if not task.onPlanning and not cur_user.get_profile().hasAccess(task, 'view'):
            raise Http404(u'Нет прав для просмотра задачи')

        error = ''
        cid = int(request.GET.get('confirm', 0))
        if cid:
            try:
                message = PM_Task_Message.objects.get(pk=cid, task=task)
                if message.code == 'SET_PLAN_TIME':
                    planTime = PM_User_PlanTime.objects.get(task=task, user=message.author)

                    authorProf = message.author.get_profile()

                    if not authorProf.hasRole(task.project, not_guest=True):
                        authorProf.setRole('employee', task.project)
                        if authorProf.is_outsource:
                            Agreement.objects.get_or_create(
                                payer=task.project.payer,
                                resp=authorProf.user
                            )

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
                elif message.code == 'TIME_REQUEST':
                    if not message.requested_time_approved:
                        if prof and prof.user.id == message.project.payer.id or prof.isManager(message.project):
                            message.requested_time_approved = True
                            message.requested_time_approve_date = datetime.datetime.now()
                            message.requested_time_approved_by = request.user
                            message.save()

                return {'redirect': task.url}
            except PM_Task_Message.DoesNotExist:
                pass
            except PM_User_PlanTime.DoesNotExist:
                pass


        winner = task.getWinner()

        setattr(task, 'text_formatted', TextFilters.getFormattedText(task.text) if task.text else '')
        # setattr(task, 'responsibleList', task.responsible.all())
        setattr(task, 'observersList', task.observers.all())
        setattr(task, 'currentWinner', winner)
        setattr(task, 'taskPlanTime', task.planTime)

        if cur_user.is_authenticated():
            setattr(task, 'canSetOnPlanning', task.onPlanning or task.canEdit(cur_user))
            setattr(task, 'canSetPlanTime', task.canPMUserSetPlanTime(prof))
            setattr(task, 'canObserve', cur_user.is_authenticated())
            setattr(task, 'canSetCritically', task.canEdit(cur_user))
            setattr(task, 'canSetReady', prof.hasRole(task.project))
            setattr(task, 'canEdit', task.canEdit(cur_user))
            setattr(task, 'canRemove', task.canPMUserRemove(prof))
            setattr(task, 'canApprove', cur_user.id == task.author.id or prof.isManager(task.project) or cur_user.is_superuser)
            setattr(task, 'canClose', task.canApprove)
            setattr(task, 'canConfirm', cur_user.is_authenticated() and task.donations.filter(user=cur_user).count())


        setattr(task, 'taskResp', [{'id': task.resp.id, 'name': task.resp.first_name + ' ' + task.resp.last_name if task.resp.first_name else task.resp.username} if task.resp else {}])

        allTime = task.getAllTime()
        files = taskExtensions.getFileList(task.files.all())

        if task:
            #set task readed
            if cur_user.is_authenticated():
                if not cur_user.id in [u.id for u in task.viewedUsers.all()]:
                    task.viewedUsers.add(cur_user)

            hiddenSubTasksExist = False
            arFilter = {
                'parentTask': task
            }

            subtasks = []
            # subtasks = taskList(request, headerValues, {'filter': arFilter}, [], {})
            # subtasks = subtasks['tasks']
            # for subtask in subtasks:
            #     if subtask['closed']:
            #         hiddenSubTasksExist = True
            #         break

        # users = widgetManager.getResponsibleList(request.user, headerValues['CURRENT_PROJECT'])
        users = User.objects.order_by('last_name').filter(
            pk__in=PM_Task_Message.objects.filter(task=task).values('author__id')
        )

        candidates = User.objects.order_by('last_name').filter(
            pk__in=PM_Task_Message.objects.filter(task=task, code='RESULT').values('author__id')
        )

        dict = task.__dict__

        for field, val in dict.iteritems():
            if isinstance(val, datetime.datetime):
                setattr(task, field, val.strftime('%d.%m.%Y %H:%M'))


        messages = task.messages.order_by('-dateCreate').exclude(code="WARNING")

        if not cur_user.is_authenticated():
            messages = messages.filter(isSystemLog=True)
        else:
            # userRoles = PM_ProjectRoles.objects.filter(user=request.user, role__code='manager')
            if not request.user.is_superuser:
                messages = messages.exclude(code="RESULT")
                messages = messages.filter(Q(hidden=False) | Q(userTo=request.user.id) | Q(author=request.user.id))


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
        arBugs = []
        for mes in messages:
            if mes.todo:
                arTodo.append({
                    'id': mes.id,
                    'text': mes.text,
                    'checked': mes.checked
                })

            if mes.bug:
                arBugs.append({
                    'id':mes.id,
                    'text': mes.text,
                    'checked': mes.checked
                })

            ob = {
                'init': True
            }
            if cur_user.is_authenticated():
                ob['canEdit'] = mes.canEdit(cur_user)
                ob['canDelete'] = mes.canDelete(cur_user)

                if mes.userTo and mes.userTo.id == cur_user.id:
                    mes.read = True
                    mes.save()

                if cur_user.get_profile().isManager(task.project):
                    ob.update({
                        'hidden_from_clients': mes.hidden_from_clients,
                        'hidden_from_employee': mes.hidden_from_employee
                    })

            setattr(mes, 'json', json.dumps(mes.getJson(ob, cur_user if cur_user.is_authenticated() else None)))

        # try:
        #     startedTimer = PM_Timer.objects.get(task=task, dateEnd__isnull=True)
        # except PM_Timer.DoesNotExist:
        #     startedTimer = None

        startedTimer = None
        setattr(task, 'todo', arTodo)
        setattr(task, 'bug', arBugs)
        templates = templateTools.getMessageTemplates()
        taskTemplate = templateTools.get_task_template()
        backers = User.objects.filter(
            pk__in=PM_Project_Donation.objects.filter(task=task)
                .values_list('user__id', flat=True)
        )

        aBackers = []
        from tracker.settings import GIFT_USD_RATE
        arDonateSum = 0
        arDonateQty = 0
        for backer in backers:
            setattr(backer, 'donated', backer.get_profile().get_donation_sum(taskId=task.id) * GIFT_USD_RATE)
            arDonateSum += backer.donated
            arDonateQty += 1
            aBackers.append(backer)

        aBackers.sort(key=lambda x: -x.donated)

        askers = []
        maxRequested = 100
        askedMin = 0
        askedMax = 0
        for m in task.messages.filter(requested_time_approved=True):
            if maxRequested < m.requested_time:
                maxRequested = m.requested_time
            askers.append({
                'user': m.author,
                'ask': m.requested_time
            })

            if not askedMin or askedMin > m.requested_time:
                askedMin = m.requested_time

            if askedMax < m.requested_time:
                askedMax = m.requested_time

        askers.sort(key=lambda x: x['ask'])

        results = []
        if task.project.id != 1131 or request.user.is_superuser:
            for m in task.messages.filter(code='RESULT'):
                if maxRequested < m.requested_time:
                    maxRequested = m.requested_time

                results.append(m)

        if maxRequested:
            maxRequested += maxRequested * 0.1

        for asker in askers:
            asker['percent'] = asker['ask'] * 100 / maxRequested

        team = []
        userShares = {}
        if task.project.blockchain_state:
            try:
                state = json.loads(task.project.blockchain_state)
                userShares = state['Users']
                teamWallets = userShares.keys()
            except ValueError:
                teamWallets = []

            t = PM_User.objects.filter(blockchain_wallet__in=teamWallets)
            for u in t:
                setattr(u, 'percent', userShares[u.blockchain_wallet])
                team.append(u)


        # brain = TaskMind()
        return {
            'projectTeam': team,
            'title': task.name,
            'task': task,
            'voted': PM_Task_Message.objects.filter(code='VOTE', author=request.user.id, task=task).exists(),
            'donated': PM_Task_Message.objects.filter(code='DONATION', author=request.user.id, task=task).exists(),
            'todo': task.messages.filter(todo=True),
            'asked_min': askedMin,
            'asked_max': askedMax,
            'donatedPercent': task.donated * 100 / maxRequested,
            'startedTimerExist': startedTimer != None,
            'startedTimerUserId': startedTimer.user.id if startedTimer else None,
            'project': task.project,
            'is_employee': cur_user.get_profile().isEmployee(task.project) if cur_user.is_authenticated() else False,
            'is_manager': cur_user.get_profile().isManager(task.project) if cur_user.is_authenticated() else False,
            'user_roles': cur_user.get_profile().getRoles(task.project) if cur_user.is_authenticated() else False,
            'files': files,
            'time': allTime,
            'avgDonate': (arDonateSum * 0.5 / (arDonateQty or 1)) if arDonateSum else 5,
            'backers': aBackers,
            'askers': askers,
            'results': results,
            'subtasks': subtasks,
            'taskTemplate': taskTemplate,
            'users': users,
            'candidates': candidates,
            'messages': messages,
            # 'solutions': similar_solutions(task.id),
            'lamp': lamp,
            'hiddenSubTasksExist': hiddenSubTasksExist,
            'templates': templates,
            'error': error
            # 'dataSet': len(arParams),
            # 'similarSet': len(tasksSimilar),
            # 'params': arParams
        }