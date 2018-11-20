# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
import datetime
from PManager.models import PM_Task, PM_Project, Tags,PM_User, PM_Timer, listManager, ObjectTags, PM_User_PlanTime, \
    PM_Milestone, PM_ProjectRoles, PM_Reminder, Release, PM_MilestoneChanges
from django.contrib.auth.models import User
from PManager.viewsExt.tools import templateTools, taskExtensions, TextFilters
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from PManager.viewsExt.tasks import TaskWidgetManager
# from tracker.settings import COMISSION
from django.db.models import Sum
from PManager.services.task_list import task_list_prepare, tasks_to_tuple
from django.db.models import Q
# This function are used in many controllers.
# It must return only json serializeble values in 'tasks' array
from tracker.settings import GIFT_USD_RATE

def get_user_tag_sums(arTagsId, currentRecommendedUser, users_id=[]):
    userTagSums = dict()
    if len(arTagsId) > 0:

        #only filtered users
        strFilterUsers = ''
        if users_id:
            strFilterUsers = ' AND object_id in ('
            c = len(users_id)
            for i, uid in enumerate(users_id):
                strFilterUsers += str(int(uid))
                if i < c - 1:
                    strFilterUsers += ', '
            strFilterUsers += ')'

        if ObjectTags.objects.filter(object_id__in=users_id).exists():
            from django.db import connection, transaction
            cursor = connection.cursor()
            table_name = ObjectTags._meta.db_table
            content_type_id = ContentType.objects.get_for_model(User).id
            arTagsIds_arg = ', '.join(arTagsId)
            sql = ('SELECT SUM(`weight`) as weight_sum, object_id '
                  ' from {} WHERE tag_id in (' + arTagsIds_arg + ') AND content_type_id=' + str(
                  content_type_id) +
                strFilterUsers +
                ' GROUP BY object_id ORDER BY weight_sum DESC').format(table_name)
            cursor.execute(sql)
            r= cursor.fetchall()
            for obj1 in r:
                if obj1:
                    userTagSums[str(obj1[1])] = int(obj1[0])

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
                    userTagSums[userId] = round(float((int(userTagSums[userId]) - int(minTagCount))) / float(
                        (int(maxTagCount) - int(minTagCount))), 3)

                # if userTagSums[userId] == maxTagCount or userTagSums[userId] == 1:
                #     currentRecommendedUser = userId

    return currentRecommendedUser, userTagSums


def get_task_tag_rel_array(task):
    taskTagRelArray = ObjectTags.objects.filter(object_id=task.id,
                                                content_type=ContentType.objects.get_for_model(task))
    arTagsId = [str(tagRel.tag.id) for tagRel in taskTagRelArray]
    return arTagsId


def widget(request, headerValues, widgetParams={}, qArgs=[], arPageParams={}, addFields=[]):
    

    widgetManager = TaskWidgetManager()
    filter = {}

    """ # TODO REDUNDANT filter=False ever
    if filter:
        lManager = listManager(PM_Task)
        filter = lManager.parseFilter(filter)
    """

    needTaskList = False
    if 'filter' in widgetParams:
        filter.update(widgetParams['filter'])
        needTaskList = True

    pst = lambda n: request.POST.get(n, 0) if hasattr(request, 'POST') else None
    pSettings = {}
    if 'CURRENT_PROJECT' in headerValues and \
            headerValues['CURRENT_PROJECT'] and \
            not 'allProjects' in filter:
        project = widgetManager.getProject(headerValues['CURRENT_PROJECT'])
        pSettings = project.getSettings()
        if project.locked:
            return {'redirect': 'payment'}

        filter['project'] = project
    else:
        if 'allProjects' in filter:
            del filter['allProjects']
        project = None
    """ # TODO: CHECK if milestone defined
    if pst('add-to-milestone'):
        tasksId = request.POST.getlist('task')
        mId = int(pst('milestone')) if pst('milestone') else 0
        mName = pst('milestone_name')
        mDate = pst('milestone_date')
        mDesc = pst('milestone_description')
        milestone = None
        if mId:
            milestone = PM_Milestone.objects.get(pk=mId)
        elif project:
            if mName:
                mName = mName.strip()
                if mDate:
                    try:
                        mDate = templateTools.dateTime.convertToDateTime(mDate)
                    except (Exception):
                        mDate = None

                if not mDate:
                    mDate = datetime.datetime.now()

                milestone = PM_Milestone(name=mName, project=project, description=mDesc)
                milestone.date = mDate
                milestone.save()

        for tId in tasksId:
            if int(tId):
                task = PM_Task.objects.get(pk=int(tId))

                if task.milestone:
                    change = PM_MilestoneChanges(milestone=task.milestone, value=-(task.planTime or 0))
                    change.save()

                task.milestone = milestone
                task.save()

                if milestone:
                    change = PM_MilestoneChanges(milestone=milestone, value=(task.planTime or 0))
                    change.save()

        return {'redirect': ''}

    elif pst('add-to-release'):
    
        tasksId = request.POST.getlist('task')
        mId = int(pst('release')) if pst('release') else 0
        mName = pst('release_name')
        mDate = pst('release_date')
        milestone = None
        if mId:
            milestone = Release.objects.get(pk=mId)
        elif project:
            if mName:
                mName = mName.strip()
                if mDate:
                    try:
                        mDate = templateTools.dateTime.convertToDateTime(mDate)
                    except (Exception):
                        mDate = None

                if not mDate:
                    mDate = datetime.datetime.now()

                milestone = Release(name=mName, project=project)
                milestone.date = mDate
                milestone.save()

        for tId in tasksId:
            if int(tId):
                task = PM_Task.objects.get(pk=int(tId))
                task.release = milestone
                task.save()

        return {'redirect': ''}
    
    #elif pst('add-observers'):
    """
    if pst('add-observers'):
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

    cur_prof = None
    aManagedProjectsId = dict()
    if cur_user.is_authenticated():
        cur_prof = cur_user.get_profile()
        try:
            aManagedProjectsId = cur_prof.managedProjects.values_list('id', flat=True)
        except AttributeError:
            aManagedProjectsId = dict()

    if not 'pageCount' in arPageParams:
        arPageParams['pageCount'] = 100
        arPageParams['page'] = 1

    tasks, paginator = {}, {}
    now = timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())

    if needTaskList:

        addTasks = {}

        if not 'parentTask' in filter and \
                not 'pk' in filter and \
                not 'isParent' in filter and \
                not 'all' in filter:
            filter['parentTask_id__isnull'] = True
        else:
            if 'pageCount' in arPageParams:
                del arPageParams['pageCount'] #выводим все подзадачи, а не только кусок, как для задач

        if 'exclude' in widgetParams:
            filter['exclude'] = widgetParams['exclude']

        arTaskOrderParams = {
            'group': arPageParams.get('group', None)
        }
        if arTaskOrderParams['group'] == 'milestones':
            filter['closed'] = False
        tasks = PM_Task.getForUser(cur_user, project, filter, qArgs, arTaskOrderParams)
        try:
            tasks = tasks['tasks']
            tasks = tasks.select_related('resp', 'project', 'milestone', 'parentTask__id', 'author', 'status','tag', 'tags__tag')
            qty = tasks.count()

        except AttributeError:
            qty = 0
            tasks = []
        if 'page' not in arPageParams:
            arPageParams['page'] = 1

        paginator = {}
        if 'pageCount' in arPageParams:
            tasks = tasks[
                    (arPageParams['page'] - 1) * arPageParams['pageCount']: arPageParams['page'] * arPageParams[
                        'pageCount']]

            paginator = {
                'all_qty': qty,
                'lastPage': (qty <= arPageParams['page'] * arPageParams['pageCount'])
            }

        currentRecommendedUser = None
        arBIsManager = {}

        arBets = {}
        arClientBets = {}
        # aUsersHaveAccess = []
        # if cur_user.is_authenticated():
        #     widgetManager.getResponsibleList(cur_user, None).values_list('id', flat=True)

        for task in tasks:
            if not task.id in arBIsManager:
                arBIsManager[task.id] = task.project.id in aManagedProjectsId

            # currentRecommendedUser, userTagSums = get_user_tag_sums(get_task_tag_rel_array(task), currentRecommendedUser,
            #                                                         aUsersHaveAccess)

            last_message_q = task.messages
            if not arBIsManager[task.id]:
                last_message_q = last_message_q.filter(
                    hidden=False, hidden_from_clients=False, hidden_from_employee=False, isSystemLog=False
                )
            last_message_q = last_message_q.order_by("-pk")

            # Yegor comment PM_Timer Deprecated
            # try:
            #     startedTimer = PM_Timer.objects.get(task=task, dateEnd__isnull=True)
            # except PM_Timer.DoesNotExist:
            #     startedTimer = None


            if 'parentTask' not in filter:
                # subtasksQuery = PM_Task.objects.filter(parentTask=task, active=True)
                filterQArgs = PM_Task.getQArgsFilterForUser(cur_user, task.project)
                filterQArgs = PM_Task.mergeFilterObjAndArray(
                    {'parentTask': task, 'active': True},
                    filterQArgs
                )
                subtasksQuery = PM_Task.objects.filter(*filterQArgs).distinct()
                subtasksQty = subtasksQuery.count()

                subtasksActiveQuery = subtasksQuery.filter(closed=False).distinct()
                subtasksActiveQty = subtasksActiveQuery.count()
            else:
                subtasksQty = 0
                subtasksActiveQty = 0

            responsibleSequence = None
            if subtasksQty:
                subtaskPlanTime = 0
                for t in subtasksQuery.annotate(summ=Sum('planTime')):
                    subtaskPlanTime += t.summ if t.summ else 0

                if subtasksActiveQty:
                    responsibleSequence = []
                    idSequence = []
                    for stask in subtasksActiveQuery.filter(resp__isnull=False):
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
                bCanBaneUser = True

            last_mes = last_message_q[0] if last_message_q else None
            addTasks[task.id] = {
                'url': task.url,
                'project': {
                    'name': task.project.name,
                    'id': task.project.id,
                },
                'author': {
                    'first_name': task.author.first_name,
                    'last_name': task.author.last_name
                },
                'donated': task.donated,
                'asked': task.asked,
                'canEdit': task.canEdit(cur_user) if cur_user.is_authenticated() else False,
                'canRemove': task.canPMUserRemove(cur_prof) if cur_prof else False,
                'canSetOnPlanning': arBIsManager[task.id] or cur_user.id == task.author.id,
                'canObserve': cur_user.is_authenticated(),
                'canApprove': arBIsManager[task.id] or cur_user.id == task.author.id,
                #todo: разрешать платным пользователям только если денег хватает
                'canClose': (cur_user.is_superuser or cur_user.id == task.author.id) if cur_user else False,
                'canSetReady': cur_prof.hasRole(task.project) and task.messages.filter(author=cur_user).exists() if cur_prof else False,
                'canSetCritically': arBIsManager[task.id] or cur_user.id == task.author.id if cur_user.is_authenticated() else False,
                'canSetPlanTime': task.canPMUserSetPlanTime(cur_prof) if cur_prof else False,
                'canBaneUser': bCanBaneUser,
                # PM_TIMER deprecated
                #'startedTimerExist': startedTimer != None,
                #'startedTimerUserId': startedTimer.user.id if startedTimer else None,
                'status': task.status.code if task.status else '',
                'todo': [
                    {
                        'todo': t['todo'],
                        'bug': t['bug'],
                        'checked': t['checked']
                    } for t in task.messages.filter(Q(Q(todo=True) | Q(bug=True))).order_by('id').values('checked', 'bug', 'todo')
                ],
                'resp': responsibleSequence if responsibleSequence else [
                    {
                        'id': task.resp.id,
                        'name': task.resp.first_name + ' ' + task.resp.last_name if task.resp.first_name else task.resp.username
                    } if task.resp else {}
                ],
                'last_message': {
                    'text': TextFilters.escapeText(last_mes.text),
                    'date': last_mes.dateCreate,
                    #todo: исправить говнокод на метод сообщения getLastTextObject
                    'author': last_mes.author.first_name + ' ' + last_mes.author.last_name if
                    last_mes.author else '',
                } if last_mes and last_mes.author else {'text': task.text},
                # 'responsibleList': userTagSums,
                'files': taskExtensions.getFileList(task.files.all()),
                'planTimes': [],
                'viewed': (task.closed or task.isViewed(cur_user)) if cur_user.is_authenticated() else False,
                'parent': task.parentTask.id if task.parentTask and hasattr(task.parentTask, 'id') else None,
                'parentName': task.parentTask.name if task.parentTask and hasattr(task.parentTask, 'name') else '',
                'subtasksQty': subtasksQty,
                'resultsQty': task.messages.filter(code='RESULT').count(),
                'subtasksActiveQty': subtasksActiveQty,
                'observer': True if task.observers.filter(id=cur_user.id) else False,
                'avatar': task.resp.get_profile().avatar_rel if task.resp else {},
                'milestoneId': task.milestone.id if task.milestone else None,
                'group': {
                    'name': task.milestone.name,
                    'id': task.milestone.id,
                    'description': task.milestone.description,
                    'code': 'milestone',
                    'closed': task.milestone.closed,
                    'date': templateTools.dateTime.convertToSite(task.milestone.date, '%d.%m.%Y')
                } if task.milestone and arPageParams.get('group') == 'milestones' else {}  #overrides by projects
            }

            if not project:
                addTasks[task.id]['group'] = {
                    'name': task.project.name,
                    'id': task.project.id,
                    'code': 'project',
                    'url': task.project.taskListUrl
                }

            if subtasksQty:
                addTasks[task.id]['planTime'] = subtaskPlanTime

            addTasks[task.id]['needRespRecommendation'] = (
                len(addTasks[task.id]['resp']) <= 0 or
                not addTasks[task.id]['resp'][0]
            )

            task_tags = task.tags.filter(tag__is_public=True)
            list_tags =[]
            if task_tags.exists():
                
                for tag in task_tags.values('tag__id','tag__tagText'):
                    list_tags.append({
                        'tagText':tag['tag__tagText'],
                        'id':tag['tag__id']
                        })
            addTasks[task.id]['tags']=list_tags

            if cur_user.is_authenticated():
                reminder = PM_Reminder.objects.filter(task=task, user=cur_user).order_by('-date').values_list('date', flat=True)
                if reminder.exists():
                    addTasks[task.id]['reminder'] = reminder[0]

            # if addTasks[task.id]['needRespRecommendation']:
            #     if currentRecommendedUser:
            #         recommendedUser = User.objects.get(pk=int(currentRecommendedUser))
            #         recommendedUserArray = {
            #             'id': recommendedUser.id,
            #             'name': recommendedUser.first_name + ' ' + recommendedUser.last_name
            #         }
            #         addTasks[task.id]['recommendedUser'] = {
            #             'id': int(currentRecommendedUser),
            #             'name': recommendedUserArray['name']
            #         }
            # TODO: DISABLE PLANTIME ? 
            # planTimes = PM_User_PlanTime.objects.filter(task=task).distinct()
            # for obj in planTimes:
            #     addTasks[task.id]['planTimes'].append({
            #         'user_url': obj.user.get_profile().url,
            #         'user_id': obj.user.id,
            #         'user_name': obj.user.first_name + ' ' + obj.user.last_name,
            #         'time': obj.time
            #     })

            #     if not task.planTime and obj.user.id == cur_user.id:
            #         addTasks[task.id]['planTime'] = obj.time

    aUserLinks = dict()
    resps = widgetManager.getResponsibleList(cur_user, project)
    aResps = []
    for resp in resps:
        histasksQty = resp.todo.filter(active=True, closed=False).count()
        setattr(resp, 'openTasksQty', histasksQty)
        if resp.id not in aUserLinks:
            try:
                aUserLinks[resp.id] = {
                    'url': resp.get_profile().url,
                    'name': resp.last_name + ' ' + resp.first_name,
                }
                aResps.append(resp)
            except PM_User.DoesNotExist:
                pass

    if needTaskList:
        aTasksId = addTasks.keys()
        if aTasksId:
            #todo: all queries
            aTimers = PM_Task.getAllTimeOfTasksWithSubtasks(aTasksId)
            tasks = tasks_to_tuple(tasks, addFields)
            tasks = task_list_prepare(tasks, addTasks, False)

            for task in tasks:
                task['time'] = 0
                task['timers'] = []
                if task['id'] in aTimers:
                    task['time'] = sum(aTimers[task['id']].values())
                    for uid in aTimers[task['id']]:
                        if uid in aUserLinks.keys():
                            task['timers'].append({
                                'time': templateTools.dateTime.timeFromTimestamp(aTimers[task['id']][uid]),
                                'user': aUserLinks[uid]['name'],
                                'user_url': aUserLinks[uid]['url']
                            })
                task['full'] = True

    today = timezone.make_aware(datetime.datetime.today(), timezone.get_current_timezone())
    yesterday = timezone.make_aware(datetime.datetime.today() - datetime.timedelta(days=1),
                                    timezone.get_current_timezone())
    template = templateTools.get_task_template()

    title = u'All tasks' if not project else project.name + ' / Tasks'
    header = u'All tasks' if not project else '<a href="/project/'+str(project.id)+'/public/">' + project.name + '</a>' + ' / Tasks'

    result = {
        'title': title,
        'header': header,
        'tasks': tasks,
        'project': project,
        'users': aResps,
        'bounty': widgetParams.get('bounty'),
        'projectSettings': pSettings,
        'tab': True,
        'name': u'Tasks',
        'paginator': paginator,
        # TODO: milestones disabled 
        #'milestones': PM_Milestone.objects.filter(project=project, closed=False),
        # TODO: releases disabled 
        #'releases': Release.objects.filter(project=project, status='new'),
        'nextPage': arPageParams.get('startPage', 0) + 1 if 'startPage' in arPageParams else None,
        'filterDates': {
            'today': templateTools.dateTime.convertToSite(today, '%d.%m.%Y'),
            'yesterday': templateTools.dateTime.convertToSite(yesterday, '%d.%m.%Y'),
        },
        'canInvite': cur_prof.isManager(project) if project and cur_prof else False,
        'template': template,
        'tags': list(Tags.objects.filter(is_public=True).values('id', 'tagText')),
    }

    if cur_user.is_authenticated():
        result['qty'] = {
            'ready': PM_Task.getQtyForUser(cur_user, project,
                                           {'status__code': 'ready', 'closed': False, 'active': True}),
            'started': PM_Task.getQtyForUser(cur_user, project,
                                             {'realDateStart__isnull': False, 'closed': False, 'active': True}),
            'not_approved': PM_Task.getQtyForUser(cur_user, project,
                                                  {'status__code': 'not_approved', 'closed': False, 'active': True}),
            'deadline': PM_Task.getQtyForUser(cur_user, project,
                                              {'deadline__lt': now, 'deadline__isnull': False,
                                               'closed': False, 'active': True})
        }
    return result
