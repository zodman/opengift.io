# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from PManager.models import Credit, Payment, PM_Task, PM_Timer, PM_Role, PM_Project, PM_User_Achievement, LogData, PM_User
from PManager.widgets.tasklist.widget import widget as taskList
from PManager.models.keys import *
from django.db.models import Q
from PManager.viewsExt.tools import templateTools
from django.contrib.auth.models import User
import datetime
from PManager.classes.git.gitolite_manager import GitoliteManager
from tracker.settings import USE_GIT_MODULE

def widget(request, headerValues, ar, qargs):
    get = request.GET
    post = request.POST
    user = {}
    if 'id' in get:
        try:
            user = User.objects.get(pk=int(get['id']))
            profile = user.get_profile()
            cur_prof = request.user.get_profile()
            if 'action' in post:
                #add this user to project
                if post['action'] == 'add_to_project':
                    project = post.get('project', None)
                    role = post.get('role', None)
                    if role and project:
                        try:
                            project = PM_Project.objects.get(id=project)
                            role = PM_Role.objects.get(id=role)
                            if cur_prof.isManager(project):
                                profile.setRole(role.code, project)
                                if USE_GIT_MODULE:
                                    GitoliteManager.regenerate_access(project)
                                return {
                                    'redirect': u'/user_detail/?id=' + unicode(get['id'])
                                }

                        except PM_Project.DoesNotExist:
                            raise u'Project does not exist'
                        except PM_Role.DoesNotExist:
                            raise u'Role does not exist'
                elif post['action'] == 'delete_user':
                    if request.user.is_superuser or request.user.is_staff and not user.is_staff:
                        user.is_active = False
                        user.save()

                        return {
                                    'redirect': u'/user_list/'
                                }
                    else:
                        raise Exception(u'Нет прав для удаления прльзователя')

            if profile.avatar:
                profile.avatar = str(profile.avatar).replace('PManager', '')
            #проекты, к которым пользователь имеет доступ
            currentUserAccessProjects = cur_prof.getProjects()
            currentUserManagedProjects = cur_prof.getProjects(only_managed=True)

            tasksResult = taskList(
                request,
                headerValues, {
                    'filter': {
                        'resp': user,
                        'closed': False,
                        'allProjects': True
                    }
                },
                [Q(Q(project__in=currentUserManagedProjects) | Q(author=request.user) | Q(resp=request.user))]
            )

            tasksObserverResult = taskList(
                request,
                headerValues, {
                    'filter': {
                        'observers': user,
                        'closed': False,
                        'allProjects': True
                    }
                },
                [Q(Q(project__in=currentUserManagedProjects) | Q(author=request.user) | Q(resp=request.user))]
            )

            taskSum = PM_Task.objects.filter(resp=user, closed=False, dateClose__isnull=True, active=True, project__in=currentUserAccessProjects).count()
            taskSumPerMonth = PM_Task.objects.filter(
                resp=user,
                active=True,
                dateClose__gt=(datetime.datetime.now()-datetime.timedelta(weeks=4)),
                project__in=currentUserAccessProjects
            ).count()

            rest, sum = 0, 0
            # sp_price = int(profile.sp_price) if profile.sp_price else 0
            arUserBets = []
            for project in currentUserAccessProjects.filter(pk__in=currentUserAccessProjects):
                timers = PM_Timer.objects.raw(
                    'SELECT SUM(`seconds`) as summ, id, user_id from PManager_pm_timer' +
                    ' WHERE `user_id`=' + str(int(user.id)) +
                    ' AND task_id in ' +
                          '(SELECT id FROM PManager_pm_task WHERE `project_id`=' + str(int(project.id)) + ')'
                )

                projectBet = profile.getBet(project)
                projectHours = 0
                for timer in timers:
                    if timer.summ:
                        sumHours = float("%.2f" % (float(timer.summ)/3600))
                        sum += sumHours
                        projectHours += sumHours
                        # rest += sumHours * (projectBet if projectBet else sp_price)
                projPrice = 0
                for o in Credit.objects.raw(
                        'SELECT SUM(`value`) as summ, id, user_id, project_id from PManager_credit' +
                        ' WHERE `user_id`=' + str(int(user.id)) +
                        ' AND `project_id`=' + str(int(project.id))
                    ):
                    p = Payment.objects.raw(
                        'SELECT SUM(`value`) as summ, id from PManager_payment' +
                        ' WHERE `user_id`=' + str(int(user.id)) +
                        ' AND `project_id`=' + str(int(project.id))
                    )
                    p = p[0].summ if p and p[0] and p[0].summ else 0
                    projPrice += o.summ - p if o.summ else 0

                # rest += projPrice

                arUserBets.append({'project': project.name, 'price': projPrice, 'bet': projectBet})


            # paid = profile.paid if profile.paid else 0
            # for o in Payment.objects.raw(
            #         'SELECT SUM(`value`) as summ, id, user_id from PManager_credit' +
            #         ' WHERE `user_id`=' + str(int(user.id))
            #     ):
            #     rest += o.summ if o.summ else 0
            #
            # for o in Payment.objects.raw(
            #         'SELECT SUM(`value`) as summ, id, user_id from PManager_payment' +
            #         ' WHERE `user_id`=' + str(int(user.id))
            #     ):
            #     paid += o.summ if o.summ else 0

            setattr(profile, 'sp', {
                'summ': sum,
                'rest': profile.account_total
            })

            userTimes = PM_Timer.objects.filter(user=user.id, task__project__id__in=currentUserAccessProjects).order_by('-id')[:20]
            if USE_GIT_MODULE:
                userKeys = Key.objects.filter(user=user.id).order_by('-id')
            else:
                userKeys = []
            userRoles = [role for role in user.userRoles.filter(project__in=currentUserAccessProjects)]

            taskTemplate = templateTools.getDefaultTaskTemplate()

            for task in tasksResult['tasks']:
                task['name'] = '<b>' + task['project']['name'] + '</b>: ' + task['name']

            for task in tasksObserverResult['tasks']:
                task['name'] = '<b>' + task['project']['name'] + '</b>: ' + task['name']

            userProjects = profile.getProjects().filter(pk__in=currentUserAccessProjects)
            for project in userProjects:
                setattr(project, 'canEdit', cur_prof.isManager(project))
                setattr(project, 'roles', [role.role.code for role in userRoles if role.project.id == project.id])


            now = datetime.date.today()
            week = [now]
            for i in range(7):
                now = now - datetime.timedelta(days=1)
                week.append(now)

            week = week[::-1]

            timeGraph = []
            arWeekDays = {
                1:u'Пн',
                2:u'Вт',
                3:u'Ср',
                4:u'Чт',
                5:u'Пт',
                6:u'Сб',
                7:u'Вс',
            }
            for date in week:
                time = LogData.objects.raw(
                    'SELECT SUM(`value`) as summ, id, user_id from PManager_logdata WHERE `user_id`=' + str(int(user.id)) + '' +
                    ' AND DATE(datetime) = \'' + date.isoformat() + '\'' +
                    ' AND code = \'DAILY_TIME\''
                )

                allTime = 0
                for timer in time:
                    allTime += timer.summ if timer.summ else 0

                date_range = (
                    datetime.datetime.combine(date, datetime.time.min),
                    datetime.datetime.combine(date, datetime.time.max)
                )

                tasksClosed = LogData.objects.filter(code='DAILY_TASKS_CLOSED', user=user, datetime__range=date_range).count()
                timeGraph.append({
                    'date': arWeekDays.get(date.isoweekday(), ''),
                    'time': str(round(allTime / 3600, 2)).replace(',', '.'),
                    'tasksClosed': tasksClosed
                })

            return {
                'user': user,
                'profile': profile,
                'achievements': [acc.achievement for acc in PM_User_Achievement.objects.filter(user=user)],
                'timers': [
                    {
                        'id': timer.id,
                        'date': timer.dateEnd,
                        'time': unicode(timer),
                        'task': timer.task.name,
                        'comment': timer.comment,
                        'task_url': timer.task.url
                    } for timer in userTimes
                ],
                'use_git': USE_GIT_MODULE,
                'keys': [
                    {
                        'id': key.id,
                        'created_at': key.created_at,
                        'name': key.name
                    } for key in userKeys
                ],
                'bets': arUserBets,
                'project_roles': userRoles,
                'user_projects': userProjects,
                'userIsEqualCurrentUser': request.user.id == user.id,
                'current_user_is_admin': request.user.is_superuser,
                'task': {
                    #'summ':taskSum,
                    #'summPerMonth':taskSumPerMonth,
                    'list': tasksResult,
                    'observers': tasksObserverResult
                },
                'taskSumm': taskSum,
                'taskLastMonth': taskSumPerMonth,
                'projectsForAddUser': currentUserManagedProjects.exclude(id__in=[k.project.id for k in userRoles]),
                'roles': PM_Role.objects.all(),
                'taskTemplate': taskTemplate,
                'timeGraph': timeGraph
            }
        except User.DoesNotExist:
            pass
