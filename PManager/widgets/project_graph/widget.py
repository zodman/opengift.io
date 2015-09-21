# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from PManager.models import PM_Task, PM_ProjectRoles, PM_Timer, ObjectTags, PM_Milestone
from django.db.models import Sum, Count
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth.models import User
from PManager.widgets.gantt.widget import widget as gantWidget

def widget(request, headerValues, ar, qargs):
    def get_bet_type_name(bet_type):
        bet_type_name = ''
        for type, name in aBetTypes:
            if type == bet_type:
                bet_type_name = name
        return bet_type_name

    current_project = headerValues['CURRENT_PROJECT']
    bPay = request.POST.get('pay', False)
    summ = int(request.POST.get('summ', 0) or 0)

    profile = request.user.get_profile()

    total = profile.account_total or 0
    totalProject = profile.account_total_project(current_project)

    bet = profile.sp_price

    aBetTypes = PM_ProjectRoles.type_choices

    roles = []
    realtime = 0
    isEmployee = False
    closestMilestone = None

    if current_project:
        o_roles = PM_ProjectRoles.objects.filter(user=request.user, project=current_project)
        for role in o_roles:
            setattr(role, 'bet_type_name', get_bet_type_name(role.payment_type))
            if not role.rate:
                setattr(role, 'rate', bet)

            if role.role.code == 'employee':
                isEmployee = True

            roles.append(role)

        tasks = PM_Task.objects.filter(project=current_project).aggregate(Sum('planTime'))
        realtime = PM_Timer.objects.filter(task__project=current_project).aggregate(Sum('seconds'))
        realtime = (realtime['seconds__sum'] or 0) * 100 / tasks['planTime__sum'] if tasks['planTime__sum'] else 0

        # CLOSEST MILESTONE
        closestMilestone = PM_Milestone.objects.filter(
            project=current_project,
            closed=False,
            id__in=PM_Task.getForUser(
                request.user,
                current_project,
                {
                    'closed': False,
                    'milestone__id__gt': 0
                })['tasks'].values_list('milestone__id', flat=True)
        ).order_by('date')

        if closestMilestone:
            closestMilestone = closestMilestone[0]
            if not profile.isManager(current_project) and not profile.isClient(current_project):
                aResp = [request.user.id]
            else:
                aResp = [d['resp__id'] for d in closestMilestone.tasks.values('resp__id').annotate(dcount=Count('resp__id'))]

            gantt = gantWidget(request, headerValues, {
                'resp__in': aResp,
                'virgin': True
            })
            tasksId = closestMilestone.tasks.values_list('id', flat=True)

            for task in gantt['tasks']:
                if task['id'] in tasksId:
                    if 'endTime' in task and task['endTime'] > closestMilestone.date:
                        setattr(closestMilestone, 'wouldOverdue', True)
                        break

            setattr(
                closestMilestone,
                'taskClosedPercent',
                closestMilestone.tasks.filter(
                    closed=True,
                    resp__in=aResp
                ).count() * 100 / (closestMilestone.tasks.filter(
                    resp__in=aResp
                ).count() or 1)
            )
        #END CLOSEST MILESTONE


    taskTagCoefficient = 0
    taskTagPosition = 0
    for obj1 in ObjectTags.objects.raw(
                                'SELECT SUM(`weight`) as weight_sum, `id` from PManager_objecttags WHERE object_id=' + str(
                request.user.id) + ' AND content_type_id=' + str(
            ContentType.objects.get_for_model(User).id) + ''):

        for obj2 in ObjectTags.objects.raw(
                                'SELECT COUNT(v.w) as position, id FROM (SELECT SUM(`weight`) as w, `id`, `object_id` from PManager_objecttags WHERE content_type_id=' + str(
            ContentType.objects.get_for_model(User).id) + ' GROUP BY object_id HAVING w >= ' + str(obj1.weight_sum or 0) + ') as v'):
            taskTagPosition = obj2.position + 1
            break


        taskTagCoefficient += (obj1.weight_sum or 0)
        break

    closedTaskQty = int(PM_Task.getQtyForUser(request.user, current_project, {'closed': True, 'active': True}))
    taskQty = int(PM_Task.getQtyForUser(request.user, current_project, {'active': True}))
    allTaskQty = int(PM_Task.getQtyForUser(request.user, None, {'closed': True, 'active': True}))

    projectData = {
        'allProjectPrice': totalProject,
        'allPrice': total,
        'closedTasksQty': closedTaskQty,
        'tasksQty': taskQty,
        'allTaskQty': allTaskQty,
        'taskClosedPercent': int(round(closedTaskQty * 100 / (taskQty or 1))),
        'bPay': bPay,
        'rating': profile.getRating(current_project),
        'rate': bet,
        'roles': roles,
        'isEmployee': isEmployee,
        'premiumTill': profile.premium_till if request.user.is_staff else '',
        'realTime': realtime,
        'taskTagCoefficient': taskTagCoefficient,
        'taskTagPosition': taskTagPosition,
        'closestMilestone': closestMilestone,
        'bNeedTutorial': 1 if not PM_Task.objects.filter(author=request.user).exists() else 0
    }

    return projectData