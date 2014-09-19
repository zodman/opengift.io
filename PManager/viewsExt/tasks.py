# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from django.db.models import Q
from django.db import transaction
from tracker.settings import COMISSION
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import intcomma
from django.shortcuts import HttpResponse
from PManager.models import PM_Task, PM_Timer, PM_Task_Message, PM_ProjectRoles, PM_Task_Status
import datetime, json, redis
from django.utils import simplejson, timezone
from PManager.viewsExt import headers
from PManager.viewsExt.tools import taskExtensions, emailMessage, templateTools
from PManager.viewsExt.gantt import WorkTime
from PManager.classes.server.message import RedisMessage
from PManager.classes.logger.logger import Logger
from PManager.services.mind.task_mind_core import TaskMind

FORMAT_TO_INTEGER = 1
CRITICALLY_THRESHOLD = 0.7
#decorator
def task_ajax_action(fn):
    def new(*args):
        if len(args) > 1:
            raise Exception("Method should not take arguments.")
        return fn(*args)

    return new


service_queue = redis.StrictRedis(
    host=settings.ORDERS_REDIS_HOST,
    port=settings.ORDERS_REDIS_PORT,
    db=settings.ORDERS_REDIS_DB,
    password=settings.ORDERS_REDIS_PASSWORD
).publish


def redisSendTaskUpdate(fields):
    mess = RedisMessage(service_queue,
                        objectName='task',
                        type='update',
                        fields=fields
    )
    mess.send()
def ajaxNewTaskWizardResponder(request):
    from django.shortcuts import render
    return render(request, 'task/new_task_wizard.html', {})
1
def taskListAjax(request):
    from PManager.widgets.tasklist.widget import widget as taskList
    from PManager.models import PM_Files, PM_User_PlanTime, PM_Task_Status

    headerValues = headers.initGlobals(request)
    ajaxTaskManager = taskAjaxManagerCreator(request)

    if ajaxTaskManager.tryToSetActionFromRequest():
        ajaxTaskManager.process()
        responseText = ajaxTaskManager.getResponse()

    elif request.POST.get('resp', False): #смена ответственного
        task_id = int(request.POST.get('id', 0)) #переданный id задачи
        if task_id:
            task = PM_Task.objects.filter(id=task_id).get() #вот она, задачка
            task.resp = User.objects.get(pk=int(request.POST.get('resp', False)))
            task.save()

            resp = task.resp
            responseText = ' '.join([resp.first_name, resp.last_name])

            if task.resp.email:
                arEmail = [task.resp.email if task.resp.id != request.user.id else None]

                task.sendTaskEmail('new_task', arEmail)

            task.systemMessage(
                u'изменен ответственный на ' + responseText,
                request.user,
                'NEW_RESPONSIBLE'
            )
            redisSendTaskUpdate(
                {
                    'resp': [{
                        'id': resp.id,
                        'name': responseText
                    }],
                    'viewedOnly': request.user.id,
                    'id': task.id
                }
            )

    elif request.POST.get('task_search', False) or \
            request.POST.get('action', False) or \
            request.POST.get('parent', False):
        #todo: как можно скорее перенести в actions
        from PManager.viewsExt.tools import templateTools

        search_text, action, group = request.POST.get('task_search'), request.POST.get('action',
                                                                                       False), request.POST.get('group',
                                                                                                                False)
        arFilter = {}
        arFilterExclude = {}
        if search_text:
            number = None
            if search_text.startswith(u'#') or search_text.startswith(u'№'):
                try:
                    number = int(search_text
                    .replace(u'#', '')
                    .replace(u'№', '')
                    .replace(u' ', '')
                    )
                except ValueError:
                    pass
            if number:
                arFilter['number'] = number
            else:
                arFilter['name__icontains'] = search_text

        qArgs = []

        if action == 'started':
            arFilter['realDateStart__isnull'] = False
            arFilter['closed'] = False
        elif action == 'critically':
            arFilter['critically__gt'] = CRITICALLY_THRESHOLD
            arFilter['closed'] = False
        elif action == 'deadline':
            arFilter['deadline__lt'] = datetime.datetime.now()
        elif action == 'arc':
            arFilter['closed'] = True
        elif action == 'ready':
            arFilter['status__code'] = 'ready'
            arFilter['closed'] = False
        elif action == 'not_ready':
            qArgs.append(Q(Q(status__in=PM_Task_Status.objects.exclude(code='ready')) | Q(status__isnull=True)))
            arFilter['closed'] = False
        elif action == 'all':
            pass

        if 'responsible[]' in request.POST:
            arFilter['resp__in'] = request.POST.getlist('responsible[]')
        if 'observers[]' in request.POST:
            arFilter['observers__in'] = request.POST.getlist('observers[]')
        if 'author[]' in request.POST:
            arFilter['author__in'] = request.POST.getlist('author[]')
        if 'closed[]' in request.POST:
            aClosedFlags = request.POST.getlist('closed[]')
            if 'N' not in aClosedFlags:
                arFilter['closed'] = True
            elif 'Y' not in aClosedFlags:
                arFilter['closed'] = False
        if 'viewed[]' in request.POST:
            aViewedFlags = request.POST.getlist('viewed[]')
            if 'N' not in aViewedFlags:
                arFilter['viewedUsers'] = request.user
            elif 'Y' not in aViewedFlags:
                arFilterExclude['viewedUsers'] = request.user

        aDatesTmp = []
        if 'date_create[]' in request.POST:
            aDatesTmp.append({
                'date': request.POST.getlist('date_create[]'),
                'key': 'dateCreate'
            })

        if 'date_modify[]' in request.POST:
            aDatesTmp.append({
                'date': request.POST.getlist('date_modify[]'),
                'key': 'dateModify'
            })

        if aDatesTmp:
            for dateTmp in aDatesTmp:
                if len(dateTmp['date']) == 1: #only one date
                    date = templateTools.dateTime.convertToDateTime(dateTmp['date'][0])
                    arFilter[dateTmp['key'] + '__gt'] = date
                    arFilter[dateTmp['key'] + '__lt'] = date + datetime.timedelta(days=1)
                elif len(dateTmp['date']) == 2: #from - to
                    filterDateFromTmp = templateTools.dateTime.convertToDateTime(dateTmp['date'][0])
                    filterDateToTmp = templateTools.dateTime.convertToDateTime(dateTmp['date'][1])
                    arFilter[dateTmp['key'] + '__gt'] = filterDateFromTmp
                    arFilter[dateTmp['key'] + '__lt'] = filterDateToTmp + datetime.timedelta(days=1)

        if 'parent' in request.POST:
            arFilter['parentTask'] = request.POST.get('parent')

        if action == 'deadline':
            qArgs.append(
                Q(
                    Q(deadline__gt=datetime.datetime.now()),
                    Q(closed=False)
                ) | Q(dateClose__gt=datetime.datetime.now())
            )

        page, count, startPage = int(request.POST.get('page', 1)), 10, int(request.POST.get('startPage', 0))
        if startPage:
            page = startPage

        if page > 2:
            count = 2 ** (page - 2) * 10
            page = 2

        if startPage:
            count *= 2
            page = 1

        arPageParams = {
            'pageCount': count,
            'page': page,
            'startPage': startPage,
            'group': group
        }

        tasks = taskList(request, headerValues, {'filter': arFilter, 'exclude': arFilterExclude}, qArgs, arPageParams)
        paginator = tasks['paginator']
        tasks = tasks['tasks']

        responseText = simplejson.dumps({'tasks': list(tasks), 'paginator': paginator})

    elif 'task_message' in request.POST:
        text = request.POST.get('task_message', '')
        task_id = request.POST.get('task_id', '')
        to = request.POST.get('to', None)
        task_close = request.POST.get('close', '') == 'Y'
        b_resp_change = request.POST.get('responsible_change', '') == 'Y'
        hidden = (request.POST.get('hidden', '') == 'Y' and to)
        task = PM_Task.objects.get(id=task_id)

        files = request.FILES.getlist('file') if 'file' in request.FILES else []
        profile = request.user.get_profile()
        bIsManager = profile.isManager(task.project)
        hidden_from_employee = False
        hidden_from_clients = False
        if bIsManager: #TODO: разобраться с тем, как должно работать скрытие от автора
            hidden_from_clients = request.POST.get('hidden_from_clients', '') == 'Y'
            hidden_from_employee = request.POST.get('hidden_from_employee', '') == 'Y'

        settings = task.project.getSettings()
        if settings.get('autohide_messages', False):
            if profile.isEmployee(task.project):
                hidden_from_clients = True
            elif profile.isClient(task.project):
                hidden_from_employee = True

        status = request.POST.get('status', '') if request.POST.get('status', '') in ['ready', 'revision'] else None
        uploaded_files = request.POST.getlist('uploaded_files') if 'uploaded_files' in request.POST else []

        author = request.user
        if task:
            text = text.replace('<', '&lt;').replace('>', '&gt;')
            message = PM_Task_Message(text=text, task=task, author=author)
            message.hidden = hidden
            message.hidden_from_clients = hidden_from_clients
            message.hidden_from_employee = hidden_from_employee
            if to:
                try:
                    to = User.objects.get(pk=int(to))
                    if b_resp_change:
                        task.resp = to
                        task.save()
                    task.observers.add(to) #TODO: подумать, надо ли добавлять в наблюдатели
                    message.userTo = to
                except User.DoesNotExist:
                    pass

            message.save()

            task.setChangedForUsers(request.user)
            if status:
                task.setStatus(status)
                logger = Logger()
                logger.log(request.user, 'STATUS_' + status.upper(), 1, task.project.id)
            if task_close:
                if task.started:
                    task.Stop()
                    task.endTimer(request.user, u'Закрытие задачи')

                task.Close(request.user)
                if task.milestone and not task.milestone.closed:
                    qtyInMS = PM_Task.objects.filter(active=True, milestone=task.milestone, closed=False).count()
                    if not qtyInMS:
                        task.milestone.closed = True
                        task.milestone.save()

                if task.parentTask:
                    c = task.parentTask.subTasks.filter(closed=False).count()
                    if c == 0:
                        task.parentTask.wasClosed = True #чтобы не учитывалось время за родительскую задачу
                        task.parentTask.Close(request.user)
                        #TODO: убрать дублирование с блоком выше
                        if task.parentTask.milestone and not task.parentTask.milestone.closed:
                            qtyInMS = PM_Task.objects.filter(active=True, milestone=task.parentTask.milestone,
                                                             closed=False).count()
                            if not qtyInMS:
                                task.parentTask.milestone.closed = True
                                task.parentTask.milestone.save()
                else:
                    for stask in task.subTasks.filter(active=True):
                        if stask.started:
                            stask.Stop()
                            stask.endTimer(request.user, u'Закрытие задачи')

                        stask.Close(request.user)

            for filePost in files:
                file = PM_Files(file=filePost, authorId=request.user, projectId=headerValues['CURRENT_PROJECT'])
                file.save()
                message.files.add(file.id)

            for filePost in uploaded_files:
                try:
                    file = PM_Files.objects.get(pk=filePost)
                    message.files.add(file)
                except PM_Files.DoesNotExist():
                    pass

            arEmail = task.getUsersEmail([author.id])

            if hidden:
                arEmail = [to.email]
                # for email in arEmail:
                #     if email != to.email:
                #         arEmail.remove(email)

            else:
                if hidden_from_clients:
                    while task.author and \
                            task.author.is_active and \
                            task.author.email and \
                                    task.author.email in arEmail:
                        arEmail.remove(task.author.email)

                if hidden_from_employee:
                    if task.resp:
                        while task.resp.email and task.resp.email in arEmail:
                            arEmail.remove(task.resp.email)

            if to and hasattr(to, 'email'):
                arEmail.append(to.email)

            taskdata = {
                'task_url': message.task.url,
                'name': message.task.name,
                'dateCreate': timezone.make_aware(datetime.datetime.now(), timezone.get_current_timezone()),
                'message': {
                    'text': message.text,
                    'author': ' '.join([message.author.first_name, message.author.last_name]),
                    'file_list': taskExtensions.getFileList(message.files.all())
                }
            }

            sendMes = emailMessage('new_task_message',
                                   {
                                       'task': taskdata
                                   },
                                   'Новое сообщение в вашей задаче!'
            )

            try:
                sendMes.send(arEmail)
            except Exception:
                print 'Email has not sent'

            responseJson = message.getJson({
                'canEdit': message.canEdit(request.user),
                'canDelete': message.canDelete(request.user),
                'noveltyMark': True
            })

            mess = RedisMessage(service_queue,
                                objectName='comment',
                                type='add',
                                fields=responseJson)
            mess.send()

            taskUpdatePushData = {'viewedOnly': request.user.id, 'id': task.id}
            if status:
                taskUpdatePushData['status'] = status
            redisSendTaskUpdate(taskUpdatePushData)
            responseText = json.dumps(responseJson)

    elif request.POST.get('prop', False):
        property = request.POST.get('prop', False)
        task_id = request.POST.get('id', False)
        value = request.POST.get('val', False)
        if property and task_id:
            task = PM_Task.objects.get(id=task_id)
            #author = request.user
            sendData = {}
            if task:
                if property == "planTime" and value:
                    task.setPlanTime(value, request)

                    taskPlanPrice = request.user.get_profile().getBet(task.project) * COMISSION * float(value)
                    task.systemMessage(
                        u'оценил(а) задачу в ' + str(value) + u'ч. с опытом '
                        + str(task.getUserRating(request.user)),
                        # + u' (' + intcomma(taskPlanPrice) + u' sp)',
                        request.user,
                        'SET_PLAN_TIME'
                    )
                elif property == "to_plan":
                    task.onPlanning = True
                    sendData['onPlanning'] = True
                    task.save()
                elif property == "from_plan":
                    task.onPlanning = False
                    sendData['onPlanning'] = False
                    planTimes = PM_User_PlanTime.objects.filter(task=task).order_by('time')
                    for planTime in planTimes:
                        if planTime.user.get_profile().isEmployee(task.project):
                            task.planTime = planTime.time
                            break
                    task.save()
                elif property == "critically":
                    value = float(value)
                    bCriticallyIsGreater = task.critically < value
                    sendData['critically'] = value
                    task.critically = value
                    task.save()
                    task.systemMessage(
                        u'Критичность ' + (u'повышена' if bCriticallyIsGreater else u'понижена'),
                        request.user,
                        'CRITICALLY_' + ('UP' if bCriticallyIsGreater else 'DOWN')
                    )
                elif property == "status":
                    if task.status.code == 'not_approved':
                        try:
                            clientRole = PM_ProjectRoles.objects.get(
                                role__code='client',
                                project=task.project,
                                user__is_staff=True
                            )
                            client = clientRole.user
                            clientProfile = client.get_profile()
                            bet = clientProfile.getBet(task.project)
                            if not bet:
                                bet = task.resp.get_profile().getBet(task.project) * COMISSION
                            if request.user.id == client.id:
                                pre = u'У вас'
                            else:
                                pre = u'У клиента'
                            if clientProfile.account_total < task.planTime * bet:
                                return HttpResponse(json.dumps({
                                    'error': pre + u' недостаточно средств для подтверждения задачи'
                                }))
                        except PM_ProjectRoles.DoesNotExist:
                            pass
                    try:
                        task.setStatus(str(value))
                        task.systemMessage(
                            u'Статус изменен на "' + task.status.name + u'"',
                            request.user,
                            'STATUS_' + task.status.code.upper()
                        )
                        sendData['status'] = task.status.code
                        logger = Logger()
                        logger.log(request.user, 'STATUS_' + task.status.code.upper(), 1, task.project.id)
                    except PM_Task_Status.DoesNotExist:
                        pass

                if len(sendData) > 0:
                    sendData['id'] = task.pk
                    sendData['viewedOnly'] = request.user.id
                    redisSendTaskUpdate(sendData)

                responseText = 'ok'
            else:
                responseText = 'none'
        else:
            responseText = 'none'
    else:
        responseText = 'bad query'

    return HttpResponse(responseText)


class taskManagerCreator:
    task = None
    parentTask = None
    project = None
    fileList = []
    currentUser = None

    def __init__(self, id=None, currentUser=None):
        if id:
            try:
                self.task = PM_Task.objects.get(id=id)
            except PM_Task.DoesNotExist:
                pass

        if currentUser:
            self.currentUser = currentUser

    def fastCreateAndGetTask(self, text):
        self.task = PM_Task.createByString(text, self.currentUser, self.fileList, self.parentTask, project=self.project)
        self.task.systemMessage(u'Задача создана', self.currentUser, 'TASK_CREATE')
        settings = self.task.project.getSettings()
        if not settings.get('start_unapproved', False):
            self.task.status = PM_Task_Status.objects.get(code='not_approved')
            self.task.save()
        return self.task

    def stopUserTimersAndPlayNew(self):
        if self.task and self.currentUser:
            if self.task.status and self.task.status.code == 'not_approved':
                settings = self.task.project.getSettings()
                if settings.get('not_start_unapproved', False):
                    return False

            timers = PM_Timer.objects.filter(user=self.currentUser, dateEnd=None)
            for timer in timers:
                timer.task.Stop()
                timer.task.endTimer(self.currentUser,
                                    'Change task to <a href="' + self.task.url + '">#' + str(self.task.id) + '</a>')

            if not self.task.deadline and self.task.planTime:
                taskTimer = WorkTime(taskHours=self.task.planTime,
                                     startDateTime=timezone.make_aware(datetime.datetime.now(),
                                                                       timezone.get_default_timezone()))
                self.task.deadline = taskTimer.endDateTime #will be saved in 'Start' method

            self.task.startTimer(self.currentUser) #запускаем таймер
            self.task.Start()
            return True
        else:
            return False

    def getSimilar(self, text):
        return PM_Task.getSimilar(text, self.project)

    def closeTask(self):
        if self.task:
            pass
        else:
            return False

    def stopTimer(self, comment):
        if self.task:
            # sid = transaction.savepoint()
            self.task.Stop()
            self.task.endTimer(None, comment) #или останавливаем и сохраняем очередной
            # transaction.commit(sid)
            return True
        else:
            return False

    def addMessage(self, message):
        message = PM_Task_Message(text=u'Время: ' + unicode(self.task.currentTimer) + "\r\n" + message, task=self.task,
                                  author=self.currentUser)
        message.save()
        responseJson = message.getJson({
            'canEdit': message.canEdit(self.currentUser),
            'canDelete': message.canDelete(self.currentUser),
            'noveltyMark': True
        })

        mess = RedisMessage(service_queue,
                            objectName='comment',
                            type='add',
                            fields=responseJson
        )
        mess.send()

        self.sendEmailAboutNewMessage(message)

    def tryToRemoveMessage(self, id):
        try:
            message = PM_Task_Message.objects.get(id=id, author=self.currentUser)
            message.delete()
            return True
        except PM_Task_Message.DoesNotExist:
            return False

    def sendEmailAboutNewMessage(self, messageObject):
        arEmail = self.task.getUsersEmail([self.currentUser.id])
        #send message to all managers
        #if it is client's message
        if messageObject.task and \
                messageObject.author.get_profile().isClient(messageObject.task.project):
            for user in User.objects.filter(
                    pk__in=PM_ProjectRoles.objects.filter(
                            role__code='manager', project=messageObject.task.project
                    ).values('user__id')
            ):
                arEmail.append(user.email)
        taskdata = {
            'task_url': messageObject.task.url,
            'name': messageObject.task.name,
            'dateCreate': timezone.make_aware(datetime.datetime.now(), timezone.get_current_timezone()),
            'time': unicode(self.task.currentTimer),
            'message': {
                'text': messageObject.text,
                'author': ' '.join([messageObject.author.first_name, messageObject.author.last_name]),
                'file_list': taskExtensions.getFileList(messageObject.files.all())
            }
        }

        sendMes = emailMessage('new_task_message',
                               {
                                   'task': taskdata
                               },
                               'Новое сообщение в вашей задаче!'
        )

        try:
            sendMes.send(arEmail)
        except Exception:
            print 'Message doesn\'t send'


#todo: заменить все действия в taskListAjax на методы данного класса
class taskAjaxManagerCreator(object):
    action = None
    result = None
    taskManager = None
    globalVariables = None
    currentUser = None
    request = None

    def __init__(self, request):
        from PManager.widgets.tasklist.widget import widget as taskList

        self.globalVariables = headers.initGlobals(request)
        self.action = request.POST.get('action', None)
        self.currentUser = request.user
        self.request = request
        self.taskListWidget = taskList
        self.initTaskManager(request)

    def getRequestData(self, key=None, format=None):
        if not key:
            return self.request
        elif key in self.request.POST:
            result = self.request.POST[key]
            if format == FORMAT_TO_INTEGER:
                try:
                    result = int(result)
                except:
                    result = 0
            return result
        else:
            return None

    def tryToSetActionFromRequest(self):
        action = self.getRequestData('action')
        if action and hasattr(self, ('process_' + action)):
            self.action = action
            return True
        else:
            return False

    def setActionName(self, actionName):
        self.action = actionName

    def initTaskManager(self, request):
        task_id = self.getRequestData('id', FORMAT_TO_INTEGER)

        taskManager = taskManagerCreator(task_id, request.user)
        taskManager.project = self.globalVariables['CURRENT_PROJECT']
        if 'parent' in request.POST:
            taskManager.parentTask = request.POST['parent']

        if 'files' in request.POST:
            taskManager.fileList = request.POST.getlist('files')

        self.taskManager = taskManager

    def process(self):
        if self.action:
            self.doAction()

    def doAction(self):
        if hasattr(self, 'process_' + self.action):
            self.result = self.__getattribute__('process_' + self.action)()

    def getResponse(self):
        if self.result:
            return HttpResponse(self.result)


    @task_ajax_action
    def process_inviteUsers(self):
        aId = self.request.POST.getlist('tasks[]')
        for id in aId:
            id = int(id)
            t = PM_Task.objects.get(id=id)

            if t.canEdit(self.currentUser):
                t.onPlanning = True
                t.save()
                redisSendTaskUpdate({
                    'id': t.id,
                    'onPlanning': True
                })
        sendMes = emailMessage('invite',
               {
                   'project': self.globalVariables['CURRENT_PROJECT']
               },
               'Приглашение пользователю'
        )
        sendMes.send(['gvamm3r@gmail.com'])
        return HttpResponse(json.dumps({'result':'OK'}))

    @task_ajax_action
    def process_baneUser(self):
        from PManager.models import Credit
        t = self.taskManager.task
        user = self.currentUser
        if t.canEdit(user):
            for timer in PM_Timer.objects.filter(user=t.resp, task=t):
                timer.delete()
            for credit in Credit.objects.filter(user=t.resp, task=t):
                credit.delete()
            t.resp = None
            t.save()
            return HttpResponse(json.dumps({'result': 'OK'}))

        return HttpResponse(json.dumps({'result': 'ERROR'}))

    @task_ajax_action
    def process_ganttAjax(self):
        from PManager.widgets.gantt.widget import widget as gantt

        aFilter = {}
        if 'date_create[]' in self.request.POST:
            aDatesTmp = self.request.POST.getlist('date_create[]')
            filterDateFromTmp = templateTools.dateTime.convertToDateTime(aDatesTmp[0])
            filterDateToTmp = templateTools.dateTime.convertToDateTime(aDatesTmp[1])
            aFilter['realDateStart__gt'] = filterDateFromTmp
            aFilter['realDateStart__lt'] = filterDateToTmp + datetime.timedelta(days=1)
        hValues = {}
        if 'project' in self.request.POST:
            hValues['CURRENT_PROJECT'] = self.request.POST.get('project')

        result = gantt(self.request, hValues, {'filter': aFilter})
        return simplejson.dumps({
            'tasks': list(result['tasks'])
        })

    @task_ajax_action
    def process_taskOpen(self):
        t = self.taskManager.task
        user = self.currentUser
        if t.closed:
            t.Open()
            if t.resp:
                if not t.resp.is_active:
                    t.resp = False
                    t.save()

            if t.parentTask and t.parentTask.closed:
                t.parentTask.Open()

            t.systemMessage(u'Задача открыта', user, 'TASK_OPEN')

        return json.dumps({
            'closed': t.closed
        })

    @task_ajax_action
    def process_taskClose(self):
        t = self.taskManager.task
        user = self.currentUser
        if t.started:
            t.Stop()
            t.endTimer(user, u'Закрытие задачи')

        if not t.closed:
            taskTimers = PM_Timer.objects.filter(task=t)
            if not taskTimers.count():
                oneSecond = datetime.timedelta(seconds=1)
                taskOneSecondTimer = PM_Timer(
                    task=t,
                    user=user,
                    dateStart=datetime.datetime.now() - oneSecond,
                    dateEnd=datetime.datetime.now(),
                    seconds=1,
                    comment=u'Закрытие задачи'
                )
                taskOneSecondTimer.save()

            profile = user.get_profile()
            if profile.isClient(t.project) or profile.isManager(t.project) or t.author.id == user.id:
                t.Close(user)
                t.systemMessage(u'Задача закрыта', user, 'TASK_CLOSE')
                #TODO: данный блок дублируется 4 раза
                if t.milestone and not t.milestone.closed:
                    qtyInMS = PM_Task.objects.filter(active=True, milestone=t.milestone, closed=False)\
                        .exclude(id=t.id).count()

                    if not qtyInMS:
                        t.milestone.closed = True
                        t.milestone.save()
                if t.parentTask and not t.parentTask.closed:
                    c = t.parentTask.subTasks.filter(closed=False, active=True).count()
                    if c == 0:
                        t.parentTask.Close(user)
                        if t.parentTask.milestone and not t.parentTask.milestone.closed:
                            qtyInMS = PM_Task.objects.filter(active=True, milestone=t.parentTask.milestone,
                                                             closed=False).count()
                            if not qtyInMS:
                                t.parentTask.milestone.closed = True
                                t.parentTask.milestone.save()


                else:
                    for stask in t.subTasks.all():
                        if stask.started:
                            stask.Stop()
                            stask.endTimer(user, u'Закрытие задачи')

                        stask.Close(user)
                net = TaskMind()
                net.train([t])

            elif (not t.status) or t.status.code != 'ready':
                t.setStatus('ready')
                t.systemMessage(
                    u'Статус изменен на "' + t.status.name + u'"',
                    user,
                    'STATUS_' + t.status.code.upper()
                )

        return json.dumps({
            'closed': t.closed,
            'status': t.status.code if t.status else None
        })

    @task_ajax_action
    def process_startObserve(self):
        obs = self.taskManager.task.observers.all()
        if self.currentUser.id not in [u.id for u in obs]:
            self.taskManager.task.observers.add(self.currentUser)

        return json.dumps({'success': 'Y'})

    @task_ajax_action
    def process_stopObserve(self):
        obs = self.taskManager.task.observers.all()
        if self.currentUser.id in [u.id for u in obs]:
            self.taskManager.task.observers.remove(self.currentUser)

        return json.dumps({'success': 'Y'})

    @task_ajax_action
    def process_removeMessage(self):
        id = self.getRequestData('id')
        if self.taskManager.tryToRemoveMessage(id):
            return json.dumps({'success': 'Y'})

    @task_ajax_action
    def process_taskPlay(self):
        if self.taskManager.stopUserTimersAndPlayNew():
            task = self.taskManager.task
            aResult = {'started': True}
            if task.deadline:
                aResult['deadline'] = templateTools.dateTime.convertToSite(task.deadline)
            return json.dumps(aResult)
        else:
            return json.dumps({'error': 'Задача не подтверждена'})

    @task_ajax_action
    def process_taskStop(self):
        comment = self.getRequestData('comment')
        public = self.getRequestData('public', FORMAT_TO_INTEGER)

        if self.taskManager.stopTimer(comment):
            if public and public > 0 and comment:
                self.taskManager.addMessage(comment)

            self.taskManager.task.setChangedForUsers(self.currentUser)
            return 'ok'

    @task_ajax_action
    def process_getSimilar(self):
        text = self.getRequestData('text')
        tasks = self.taskManager.getSimilar(text)
        return json.dumps([{'name': task.name, 'url': task.url} for task in tasks])

    @task_ajax_action
    def process_fastCreate(self):
        taskInputText = self.getRequestData('task_name')
        request = self.getRequestData()
        if taskInputText:
            task = self.taskManager.fastCreateAndGetTask(taskInputText)
            if task:

                taskListWidgetData = self.taskListWidget(request, self.globalVariables, {'filter': {'id': task.id}})
                tasks = taskListWidgetData['tasks']
                if tasks:
                    return json.dumps(tasks[0])
        else:
            return json.dumps({'errorText': 'Empty task name'})

    @task_ajax_action
    def process_getUserLastOpenTask(self):
        import random

        task = PM_Task.objects.filter(
            closed=False,
            active=True,
            realDateStart__isnull=False,
            resp=self.currentUser.id,
            dateModify__lt=(datetime.datetime.now() - datetime.timedelta(minutes=1))
        ).exclude(
            status__code='ready'
        ).order_by('-critically', '-realDateStart')[:5]

        if task.count():
            taskTmp = task[random.randint(0, (task.count() - 1))]
            task = {
                'name': taskTmp.name,
                'url': taskTmp.url,
                'project__name': taskTmp.project.name
            }
            return json.dumps(task)
        else:
            return json.dumps({'user': self.currentUser.id})

    @task_ajax_action
    def process_insertBefore(self):
        taskId = self.getRequestData('id', FORMAT_TO_INTEGER)
        taskAfter = self.getRequestData('before_id', FORMAT_TO_INTEGER)

        if taskId:
            try:
                task = PM_Task.objects.get(pk=taskId)
            except PM_Task.DoesNotExist:
                return json.dumps({'error': 'task not found'})
            if not self.currentUser.get_profile().hasAccess(task, 'change'):
                return json.dumps({'error': 'access denied'})

            if taskAfter:
                try:
                    taskAfter = PM_Task.objects.get(pk=taskAfter)
                except PM_Task.DoesNotExist:
                    return json.dumps({'error': 'Parent task not found'})

                tasks = PM_Task.getForUser(self.currentUser, task.project,
                                           {
                                               'critically__gte': taskAfter.critically,
                                               'closed': False,
                                               'parentTask__isnull': True,
                                               'exclude': {'id': task.id}
                                           }, [], {'order_by': '-critically'})
                prevCriticaly = None
                taskSet = []
                secondTaskSet = []
                for eTask in tasks['tasks']:
                    taskSet.append(eTask)
                    if eTask.id == taskAfter.id:
                        if prevCriticaly and prevCriticaly > eTask.critically: #we just put cur task beyond two
                            if eTask.critically < task.critically < prevCriticaly: #if task was at the same place
                                return json.dumps({'result': 'task did not modified'})
                            else:
                                task.critically = (prevCriticaly + eTask.critically) / 2
                                task.save()
                                return json.dumps({'result': '1 task modified'})
                        elif prevCriticaly and (prevCriticaly <= 1): #previous task exist
                            secondTaskSet.append(task)
                            taskSet.reverse()
                            for uTask in taskSet:
                                secondTaskSet.append(uTask)
                                if prevCriticaly < uTask.critically:
                                    critPoint = (uTask.critically - prevCriticaly) / len(secondTaskSet)
                                    i = 0
                                    for rTask in secondTaskSet:
                                        rTask.critically = prevCriticaly + (i * critPoint)
                                        rTask.save()
                                        i += 1
                                    return json.dumps({'result': str(len(secondTaskSet)) + ' tasks modified'})

                            #if all tasks before taskAfter have similar critically (but lesser that 1)
                            critPoint = (1 - prevCriticaly) / (len(secondTaskSet) + 1)
                            i = 0
                            for rTask in secondTaskSet:
                                rTask.critically = prevCriticaly + (i * critPoint)
                                rTask.save()
                                i += 1

                            return json.dumps({'result': str(len(secondTaskSet)) + ' tasks modified'})
                        else:
                            task.critically = taskAfter.critically + 0.01
                            task.save()
                            return json.dumps({'result': '1 first task modified'})
                    prevCriticaly = eTask.critically

            return json.dumps({'result': prevCriticaly})

    @task_ajax_action
    def process_appendTask(self):
        taskId = self.getRequestData('id', FORMAT_TO_INTEGER)
        taskParent = self.getRequestData('parent_id', FORMAT_TO_INTEGER)
        if taskId:
            try:
                task = PM_Task.objects.get(id=taskId)
                task.setParent(taskParent)
                if task.parentTask:
                    task.systemMessage(u'перенесена в задачу №' + str(task.parentTask.number))
                else:
                    task.systemMessage(u'перенесена в основной список задач')
                return json.dumps({'result': 'ok'})
            except PM_Task.DoesNotExist:
                return json.dumps({'errorText': 'Task does not exist'})

    @task_ajax_action
    def process_deleteTask(self):
        taskId = self.getRequestData('id', FORMAT_TO_INTEGER)

        if taskId:
            try:
                task = PM_Task.objects.get(id=taskId)
                task.safeDelete()
                for st in task.subTasks.all():
                    st.safeDelete()
                return json.dumps({'result': 'ok', 'deleted': True})
            except PM_Task.DoesNotExist:
                return json.dumps({'errorText': 'Task does not exist'})


class TaskWidgetManager:
    def parseTaskCreateString(self, taskString):
        return {}

    @staticmethod
    def getUsersOfCurrentProject(project, aRoleCodes):
        from PManager.models import PM_ProjectRoles, PM_Role

        return User.objects.order_by('last_name').filter(
            is_active=True,
            pk__in=PM_ProjectRoles.objects.filter(
                role__in=PM_Role.objects.filter(code__in=aRoleCodes), project=project
            ).values('user__id')
        )

    @staticmethod
    def getUsersThatUserHaveAccess(user, project):
        from PManager.models import PM_Role, PM_ProjectRoles

        users = User.objects.filter(is_active=True)
        if project:
            if user.get_profile().isManager(project):
                users = users.filter(pk__in=PM_ProjectRoles.objects.filter(
                    project__in=user.get_profile().managedProjects.values('id')).values('user__id'))
            else:
                try:
                    users = users.filter(
                        pk__in=PM_ProjectRoles.objects.filter(role=PM_Role.objects.get(code='employee'),
                                                              project=project).values('user__id'))
                except PM_Role.DoesNotExist:
                    pass

        else:
            userProjects = user.get_profile().getProjects()
            users = users.filter(
                pk__in=PM_ProjectRoles.objects.filter(project__in=userProjects).values('user__id')
            )

        return users

    @staticmethod
    def getUsersThatCanBeResponsibleInThisProject(user, project):
        if user.get_profile().isManager(project):
            return TaskWidgetManager.getUsersOfCurrentProject(project, ['employee', 'manager', 'client'])
        elif user.get_profile().isClient(project):
            return TaskWidgetManager.getUsersOfCurrentProject(project, ['manager', 'client', 'employee'])
        else:
            return TaskWidgetManager.getUsersOfCurrentProject(project, ['employee', 'manager'])

    @staticmethod
    def getResponsibleList(user, project):
        return TaskWidgetManager.getUsersThatCanBeResponsibleInThisProject(user, project)

    def getProject(self, defaultProject):
        return defaultProject