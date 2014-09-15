# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
import datetime
from PManager.models import PM_Task, PM_Timer, listManager, ObjectTags, PM_User_PlanTime, PM_Milestone, PM_ProjectRoles
from django.contrib.auth.models import User
from PManager.viewsExt.tools import templateTools, taskExtensions, TextFilters
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from PManager.viewsExt.tasks import TaskWidgetManager
from tracker.settings import COMISSION

#This function are used in many controllers.
#It must return only json serializeble values in 'tasks' array
def widget(request, headerValues, widgetParams={}, qArgs=[], arPageParams={}, addFields=[]):
    widgetManager = TaskWidgetManager()
    filter = {}

    if filter:
        lManager = listManager(PM_Task)
        filter = lManager.parseFilter(filter)
    if 'filter' in widgetParams:
        filter.update(widgetParams['filter'])

    pst = lambda n: request.POST.get(n, 0) if hasattr(request, 'POST') else None
    if 'CURRENT_PROJECT' in headerValues and \
            headerValues['CURRENT_PROJECT'] and \
            not 'allProjects' in filter:
        project = widgetManager.getProject(headerValues['CURRENT_PROJECT'])
        filter['project'] = project
    else:
        if 'allProjects' in filter:
            del filter['allProjects']
        project = None

    if pst('add-to-milestone'):
        tasksId = request.POST.getlist('task')
        mId = int(pst('milestone')) if pst('milestone') else 0
        mName = pst('milestone_name')
        mDate = pst('milestone_date')

        if mId:
            milestone = PM_Milestone.objects.get(pk=mId)
        elif project:
            milestone = None
            if mName:
                mName = mName.strip()
                if mDate:
                    try:
                        mDate = templateTools.dateTime.convertToDateTime(mDate)
                    except (Exception):
                        mDate = None

                if not mDate:
                    mDate = datetime.datetime.now()

                milestone = PM_Milestone(name=mName, project=project)
                milestone.date = mDate
                milestone.save()

        for tId in tasksId:
            if int(tId):
                task = PM_Task.objects.get(pk=int(tId))
                task.milestone = milestone
                task.save()

        return {'redirect': ''}
    elif pst('add-observers'):
        #todo: объединить с выше
        tasksId = request.POST.getlist('task')
        mId = int(pst('observer')) if pst('observer') else 0
        if mId:
            observer = User.objects.get(pk=mId)
        else:
            observer = None
        if observer:
            for tId in tasksId:
                if int(tId):
                    task = PM_Task.objects.get(pk=int(tId))
                    task.observers.add(observer)
                    task.save()

        return {'redirect': ''}

    if isinstance(request, User):
        #@var User request
        cur_user = request
    else:
        #@var HttpRequest request
        cur_user = request.user

    cur_prof = cur_user.get_profile()

    if not 'pageCount' in arPageParams:
        arPageParams['pageCount'] = 100
        arPageParams['page'] = 1



    #try:
    addTasks = {}

    if not 'parentTask' in filter and \
            not 'pk' in filter and \
            not 'all' in filter:
        filter['parentTask__isnull'] = True
    else:
        arPageParams = {} #выводим все подзадачи, а не только кусок, как для задач

    arPageParams['invite'] = widgetParams.get('invite', False)
    if 'exclude' in widgetParams:
        filter['exclude'] = widgetParams['exclude']

    tasks = PM_Task.getForUser(cur_user, project, filter, qArgs, arPageParams)
    paginator = tasks['paginator']
    tasks = tasks['tasks']

    currentRecommendedUser = None
    arBIsManager = {}

    arBets = {}
    for task in tasks:
        if not task.id in arBIsManager:
            arBIsManager[task.id] = cur_prof.isManager(task.project)

        if task.resp and \
                task.planTime and \
                task.status and \
                task.status.code == 'not_approved':
            #if client have fix price
            try:
                clientBet = PM_ProjectRoles.objects.get(
                    rate__isnull=False,
                    role__code='client',
                    project=task.project,
                    payment_type='plan_time'
                )
                rate = clientBet.rate
            except PM_ProjectRoles.DoesNotExist:
                rate = task.resp.get_profile().getBet(task.project) * COMISSION

            arBets[task.id] =  task.planTime * rate

        task.time = task.getAllTime()
        taskTagRelArray = ObjectTags.objects.filter(object_id=task.id,
                                                    content_type=ContentType.objects.get_for_model(task))

        arTagsId = [str(tagRel.tag.id) for tagRel in taskTagRelArray]

        userTagSums = {}
        if len(arTagsId) > 0:
            r = ObjectTags.objects.raw(
                            'SELECT SUM(`weight`) as weight_sum, `id`, `object_id`, `content_type_id` from PManager_objecttags WHERE tag_id in (' + ', '.join(
                            arTagsId) + ') AND content_type_id=' + str(
            ContentType.objects.get_for_model(User).id) + ' GROUP BY object_id')
            for obj1 in r:
                if obj1.content_object:
                    userTagSums[str(obj1.content_object.id)] = int(obj1.weight_sum)

            minTagCount, maxTagCount = False, 0

            for userId in userTagSums:
                if maxTagCount < userTagSums[userId]: maxTagCount = userTagSums[userId]
                if minTagCount > userTagSums[userId] or minTagCount == False: minTagCount = userTagSums[userId]

            currentRecommendedUser = None
            if maxTagCount > 0:
                for userId in userTagSums:
                    if minTagCount == maxTagCount:
                        userTagSums[userId] = 1 if userTagSums[userId] == minTagCount else 0
                    else:
                        userTagSums[userId] = float((int(userTagSums[userId]) - int(minTagCount))) / float(
                            (int(maxTagCount) - int(minTagCount)))

                    if userTagSums[userId] == maxTagCount or userTagSums[userId] == 1:
                        currentRecommendedUser = userId

        now = timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())
        task_delta = task.dateModify + datetime.timedelta(days=1)
        last_message_q = task.messages
        if not arBIsManager[task.id]:
            last_message_q = last_message_q.filter(
                hidden=False, hidden_from_clients=False, hidden_from_employee=False
            )
        last_message_q = last_message_q.order_by("-pk")

        try:
            startedTimer = PM_Timer.objects.get(task=task, dateEnd__isnull=True)
        except PM_Timer.DoesNotExist:
            startedTimer = None

        if 'parentTask' not in filter:
            # subtasksQuery = PM_Task.objects.filter(parentTask=task, active=True)
            filterQArgs = PM_Task.getQArgsFilterForUser(cur_user, task.project, widgetParams.get('invite', False))
            filterQArgs = PM_Task.mergeFilterObjAndArray({'parentTask': task, 'active': True}, filterQArgs)
            subtasksQuery = PM_Task.objects.filter(*filterQArgs)
            subtasksQty = subtasksQuery.count()

            subtasksActiveQuery = subtasksQuery.filter(closed=False)
            subtasksActiveQty = subtasksQuery.filter(closed=False).count()
        else:
            subtasksQty = 0
            subtasksActiveQty = 0



        subtaskTime = task.time
        responsibleSequence = None
        if subtasksQty:
            subtaskTime = 0
            subtaskPlanTime = 0
            for t in subtasksQuery:
                subtaskTime += t.getAllTime()
                subtaskPlanTime += int(t.planTime) if t.planTime else 0

            if subtasksActiveQty:
                responsibleSequence = []
                idSequence = []
                for stask in subtasksActiveQuery:
                    if stask.resp:
                        respName = stask.resp.first_name + ' ' + stask.resp.last_name \
                            if stask.resp.first_name else stask.resp.username
                        if not stask.resp.id in idSequence:
                            idSequence.append(stask.resp.id)
                            responsibleSequence.append({
                                'id': stask.resp.id,
                                'name': respName
                            })

        bCanBaneUser = False
        if arBIsManager[task.id] and task.resp:
            lastRespMessageDate = last_message_q.filter(author=task.resp)
            lastRespMessageDate = lastRespMessageDate[0] if lastRespMessageDate else None
            if lastRespMessageDate:
                lastRespMessageDateCreate = lastRespMessageDate.dateCreate
            else:
                lastRespMessageDateCreate = task.realDateStart or task.dateCreate

            bCanBaneUser = lastRespMessageDateCreate < timezone.make_aware(
                datetime.datetime.now(), timezone.get_current_timezone()
            ) - datetime.timedelta(days=2)

        addTasks[task.id] = {
            'url': task.url,
            'time': subtaskTime,
            'project': {
                'name': task.project.name
            },
            'canEdit': task.canEdit(cur_user),
            'canRemove': task.canPMUserRemove(cur_prof),
            'canSetOnPlanning': arBIsManager[task.id] or False,
            'canApprove': arBIsManager[task.id] or request.user.id == task.author.id,
            'canSetCritically': arBIsManager[task.id] or request.user.id == task.author.id,
            'canSetPlanTime': task.canPMUserSetPlanTime(cur_prof),
            'canBaneUser': bCanBaneUser,
            'planPrice': arBets.get(task.id, 0),
            'startedTimerExist': startedTimer != None,
            'startedTimerUserId': startedTimer.user.id if startedTimer else None,
            'status': task.status.code if task.status else '',
            'resp': responsibleSequence if responsibleSequence else [
                {'id': task.resp.id, 'name': task.resp.first_name + ' ' + task.resp.last_name if task.resp.first_name else task.resp.username} if task.resp else {}
            ],
            'last_message': {
                'text': TextFilters.escapeText(last_message_q[0].text),
                'date': last_message_q[0].dateCreate,
                #todo: исправить говнокод на метод сообщения getLastTextObject
                'author': last_message_q[0].author.first_name + ' ' + last_message_q[0].author.last_name if
                last_message_q[0].author else '',
            } if last_message_q and last_message_q[0] and last_message_q[0].author else {'text': task.text},
            'responsibleList': userTagSums,
            'files': taskExtensions.getFileList(task.files.all()),
            'planTimes': [],
            'viewed': (task.closed or task.isViewed(cur_user)),
            'parent': task.parentTask.id if task.parentTask and hasattr(task.parentTask, 'id') else None,
            'subtasksQty': subtasksQty,
            'subtasksActiveQty': subtasksActiveQty,
            'observer': True if task.observers.filter(id=cur_user.id) else False,
            'group': {
                'name': task.milestone.name,
                'id': task.milestone.id,
                'code': 'milestone',
                'closed': task.milestone.closed,
                'date': templateTools.dateTime.convertToSite(task.milestone.date, '%d.%m.%Y')
            } if task.milestone and arPageParams.get('group') == 'milestones' else {} #overrides by projects
        }
        if not project:
            addTasks[task.id]['group'] = {
                'name': task.project.name,
                'id': task.project.id,
                'code': 'project'
            }

        if subtasksQty:
            addTasks[task.id]['planTime'] = subtaskPlanTime
        addTasks[task.id]['needRespRecommendation'] = now > task_delta and len(addTasks[task.id]['resp']) <= 0

        if addTasks[task.id]['needRespRecommendation']:
            if currentRecommendedUser:
                recommendedUser = User.objects.get(pk=int(currentRecommendedUser))
                recommendedUserArray = {
                    'id': recommendedUser.id,
                    'name': recommendedUser.first_name + ' ' + recommendedUser.last_name
                }
                addTasks[task.id]['recommendedUser'] = {
                    'id': int(currentRecommendedUser),
                    'name': recommendedUserArray['name']
                }

        planTimes = PM_User_PlanTime.objects.filter(task=task).distinct()
        for obj in planTimes:
            addTasks[task.id]['planTimes'].append({
                'user_url': obj.user.get_profile().url,
                'user_id': obj.user.id,
                'user_name': obj.user.first_name + ' ' + obj.user.last_name,
                'time': obj.time
            })

            if not task.planTime and obj.user.id == cur_user.id:
                addTasks[task.id]['planTime'] = obj.time

        timers = PM_Timer.objects.raw(
            'SELECT SUM(`seconds`) as summ, id, user_id from PManager_pm_timer WHERE `task_id`=' + str(int(
                task.id)) + ' GROUP BY user_id')#.filter(task=task).annotate(summ=Sum('seconds')).annotate(usercount=Count('user'))

        addTasks[task.id]['timers'] = []
        for timer in timers:
            user = timer.user
            addTasks[task.id]['timers'].append({
                'time': templateTools.dateTime.timeFromTimestamp(timer.summ),
                'user': user.last_name + ' ' + user.first_name,
                'user_url': user.get_profile().url
            })

    tasks = tasks.values(*(addFields + [
        'critically',
        'project__name',
        'planTime',
        'realTime',
        'onPlanning',
        'author__username',
        'author__first_name',
        'author__last_name',
        'name',
        'text',
        'id',
        'deadline',
        'closed',
        'started',
        'dateClose',
        'number',
        'status__code'
    ])
    )
    tasks = PM_Task.getListPrepare(tasks, addTasks, False)

    for task in tasks:
        task['full'] = True

    today = timezone.make_aware(datetime.datetime.today(), timezone.get_current_timezone())
    yesterday = timezone.make_aware(datetime.datetime.today() - datetime.timedelta(days=1),
                                    timezone.get_current_timezone())
    template = templateTools.getDefaultTaskTemplate()

    return {
        'title': (project.name + u': ' if project else u'') + u'задачи',
        'tasks': tasks,
        'project': project,
        'users': widgetManager.getResponsibleList(cur_user, project),
        'paginator': paginator,
        'milestones': PM_Milestone.objects.filter(project=project),
        'nextPage': arPageParams.get('startPage', 0) + 1 if 'startPage' in arPageParams else None,
        'filterDates': {
            'today': templateTools.dateTime.convertToSite(today, '%d.%m.%Y'),
            'yesterday': templateTools.dateTime.convertToSite(yesterday, '%d.%m.%Y'),
        },
        'template': template,
        'qty': {
            'ready': PM_Task.getQtyForUser(cur_user, project,
                                           {'status__code': 'ready', 'closed': False, 'active': True}),
            'started': PM_Task.getQtyForUser(cur_user, project,
                                             {'realDateStart__isnull': False, 'closed': False, 'active': True}),
            'critically': PM_Task.getQtyForUser(cur_user, project,
                                             {'critically__gt': 0.7, 'closed': False, 'active': True})
        },
        'isInvite': arPageParams['invite']
    }
