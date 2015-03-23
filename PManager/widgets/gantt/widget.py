# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from PManager.models import PM_Task, listManager, PM_Milestone
from django.contrib.auth.models import User
import datetime
#from django.db.models import Sum,Count
#from PManager.viewsExt.tools import templateTools
#from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db import transaction
from PManager.viewsExt.gantt import WorkTime
from PManager.models.tasks import PM_Project
from PManager.widgets.tasklist.widget import TaskWidgetManager as widgetManager
from PManager.viewsExt.tools import templateTools


@transaction.commit_manually
def flush_transaction():
    transaction.commit()

def sortGantt(a, b):
    if not a['virgin'] or not b['virgin']:
        return 0
    if a['critically'] == b['critically']:
        return 0
    return -1 if a['critically'] > b['critically'] else 1

def create_milestone_from_post(request, headerValues):
    def pst(n):
        return request.POST.get(n, '')
    try:
        project_id = pst('milestone-project')
        project = PM_Project.objects.get(pk=int(project_id))
    except (PM_Project.DoesNotExist, ValueError) as e:
        project = headerValues['CURRENT_PROJECT']
    if pst('milestone-name') != '' and project:
        name = pst('milestone-name')
        date = pst('milestone-date')
        date = templateTools.dateTime.convertToDateTime(date)
        milestone = PM_Milestone(name=name, date=date, project=project)
        milestone.save()
        return {'redirect': ''}

def widget(request, headerValues, widgetParams={}, qArgs=[]):
    from django.db.models import Q
    bProjectSelected = 'CURRENT_PROJECT' in headerValues

    create_milestone_from_post(request, headerValues)

    def getTaskResponsibleDates(aDates, task, endTime):
        if task['resp__id']:
            if not aDates.get(task['resp__id'], None) or endTime > aDates[task['resp__id']]:
                aDates[task['resp__id']] = endTime
        return aDates

    startHours = 9
    endHour = 18
    holyDays = [5, 6]
    flush_transaction()
    filter = {}
    if isinstance(request, User):
        cur_user = request
    else:
        cur_user = request.user

    if hasattr(request, 'GET'):
        if request.GET.get('filter', '') == 'Y':
            if request.GET.get('my', '') == 'Y':
                filter['resp'] = cur_user
            if request.GET.get('overdue', '') == 'Y':
                filter['deadline__lte'] = datetime.datetime.now()

    if filter:
        lManager = listManager(PM_Task)
        filter = lManager.parseFilter(filter)

    if 'CURRENT_PROJECT' in headerValues:
        filter['project'] = headerValues['CURRENT_PROJECT']
    else:
        filter['allProjects'] = True

    milestones = []
    if 'project' in filter:
        milestones = PM_Milestone.objects.filter(project=filter['project'])

    if 'filter' in widgetParams:
        filter.update(widgetParams['filter'])
    else:
        qArgs.append(Q(
            Q(realDateStart__isnull=False) | Q(closed=False)
        ))

    # if not 'parentTask' in filter:
    #     filter['parentTask__isnull'] = True

    tasks = PM_Task.getForUser(
        request.user,
        filter.get('project', 0),
        filter,
        qArgs,
        {
            'order_by': [
                '-virgin',
                '-realDateStart'
            ]
        }
    )
    tasks = tasks['tasks'].values(
        'id',
        'name',
        'realDateStart',
        'planTime',
        'closed',
        'dateCreate',
        'dateClose',
        'dateModify',
        'project__name',
        'status__code',
        'milestone__id',
        'parentTask__name',
        'resp__id',
        'virgin',
        'critically'
    )

    tasks = tasks[:400]

    aTasks = []
    responsibleLastDates = {}
    now = timezone.make_aware(datetime.datetime.now(), timezone.get_current_timezone())
    aResp = []
    for task in tasks:
        if not task['parentTask__name'] and PM_Task.objects.filter(parentTask__id=task['id'], active=True):
            continue

        if task['resp__id'] and task['resp__id'] not in aResp:
            aResp.append(task['resp__id'])

        aTasks.append(task)

    if 'project' in filter and filter['project']:
        if aResp:
            aOtherTasks = []
            otherTasks = PM_Task.objects.filter(resp__in=aResp, closed=False, active=True, project__closed=False).exclude(project=filter['project']).values(
                'id',
                'name',
                'realDateStart',
                'planTime',
                'closed',
                'dateCreate',
                'dateClose',
                'dateModify',
                'project__name',
                'status__code',
                'milestone__id',
                'parentTask__name',
                'resp__id',
                'virgin',
                'critically'
            )
            for task in otherTasks:
                if not task['parentTask__name'] and PM_Task.objects.filter(parentTask__id=task['id'], active=True).count():
                    continue

                task['name'] = ''
                aOtherTasks.append(task)
            aTasks = aOtherTasks + aTasks
            aTasks = sorted(aTasks, cmp=sortGantt)


    #сначала пробежимся по начатым задачам, чтобы выстроить остальные за ними
    for task in aTasks:
        if task['parentTask__name'] and task['name']:
            task['name'] = task['parentTask__name'] + ' / ' + task['name']

        if task['realDateStart']:
            if task['planTime']:
                taskTimer = WorkTime(
                    startDateTime=task['realDateStart'],
                    taskHours=task['planTime']
                )

                endTime = task['realDateStart'] + datetime.timedelta(hours=taskTimer.taskRealTime)
                if endTime < now and not task['closed']:
                    endTime = now

                responsibleLastDates = getTaskResponsibleDates(responsibleLastDates, task, endTime)

    aTaskMilestones = {}
    for task in aTasks:
        #если время задачи не задано, его надо расчитать
        if not task['planTime']:
            task['planTime'] = 4 #TODO: продумать, как можно сделать этот параметр динамическим

        if task['realDateStart']:
            task['dateCreateGantt'] = task['realDateStart']
        elif task['closed'] == True:
            task['dateCreateGantt'] = task['dateCreate']
        else:
            task['dateCreateGantt'] = now
            #если ответственный занят, выстраиваем в ряд
            # for resp in task['responsible']:
            if task['resp__id'] in responsibleLastDates:
                task['dateCreateGantt'] = task['dateCreateGantt'] if task['dateCreateGantt'] > responsibleLastDates[
                    task['resp__id']] else responsibleLastDates[task['resp__id']] + datetime.timedelta(hours=1)

        if task['dateClose']:
            endTime = task['dateClose']
        elif task['planTime']:
            taskTimer = WorkTime(
                startDateTime=task['dateCreateGantt'],
                taskHours=task['planTime']
            )

            endTime = task['dateCreateGantt'] + datetime.timedelta(hours=taskTimer.taskRealTime)
            if endTime < now and not task['closed']: endTime = now
        elif task['dateModify']:
            endTime = now
        else:
            endTime = task['dateCreateGantt'] + datetime.timedelta(hours=1)

        responsibleLastDates = getTaskResponsibleDates(responsibleLastDates, task, endTime)

        task['endTime'] = endTime
        if 'filter' in widgetParams: #ajax call
            task['realDateStart'] = templateTools.dateTime.convertToSite(task['realDateStart'], '%d.%m.%Y %H:%I:%S')
            task['dateCreate'] = templateTools.dateTime.convertToSite(task['dateCreate'], '%d.%m.%Y %H:%I:%S')
            task['dateCreateGantt'] = templateTools.dateTime.convertToSite(task['dateCreateGantt'], '%Y-%m-%dT%H:%I:%S')
            task['endTime'] = templateTools.dateTime.convertToSite(task['endTime'], '%Y-%m-%dT%H:%I:%S')
            task['dateClose'] = templateTools.dateTime.convertToSite(task['dateClose'], '%d.%m.%Y %H:%I:%S')
            task['dateModify'] = templateTools.dateTime.convertToSite(task['dateModify'], '%d.%m.%Y %H:%I:%S')

        if bProjectSelected:
            task['title'] = task['name']
        else:
            task['title'] = task['project__name'] + task['name']

        task['full'] = True
        task['resp__id'] = task['resp__id'] if task['resp__id'] else 0

        if task['milestone__id']:
            if task['milestone__id'] not in aTaskMilestones:
                aTaskMilestones[task['milestone__id']] = []

            aTaskMilestones[task['milestone__id']].append(task['id'])

    aMilestones = []
    aDates = []
    for milestone in milestones:
        if milestone.id in aTaskMilestones:
            setattr(milestone, 'tasksId', aTaskMilestones[milestone.id])
        if milestone.date in aDates:
            milestone.date = milestone.date + datetime.timedelta(hours=4)

        aDates.append(milestone.date)
        aMilestones.append(milestone)

    return {
        'title': u'Диаграмма Ганта',
        'tasks': aTasks,
        'milestones': aMilestones,
        'users': widgetManager.getResponsibleList(cur_user, filter['project'])
    }