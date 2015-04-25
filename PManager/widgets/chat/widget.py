# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from PManager.models import PM_Task_Message, PM_Project
from django.db.models import Q
from PManager.viewsExt.tools import templateTools
from tracker import settings


def widget(request, headerValues=None, ar=None, qargs=None):
    last_id = request.REQUEST.get('last_id', 0)
    if request.user.is_superuser:
        hiddenQ = Q(author__isnull=False)
    else:
        hiddenQ = Q(hidden=False)
    managedProjects = request.user.get_profile().getProjects(only_managed=True).values_list('id', flat=True)
    userProjects = request.user.get_profile().getProjects().values_list('id', flat=True)

    unManagedQ = Q(project__in=managedProjects)
    if len(userProjects) != len(managedProjects):
        unManagedQ = unManagedQ | Q(
                                        Q(
                                            Q(task__observers=request.user) &
                                            Q(hidden_from_clients=False) &
                                            Q(hidden_from_employee=False) |

                                            Q(task__resp=request.user) |
                                            Q(task__author=request.user)  #todo: add hidden from clients and hidden from employee
                                        ) &
                                        Q(project__in=userProjects)
                                    )

    activeProjects = PM_Project.objects.exclude(closed=True, locked=True).values_list('id', flat=True)

    result = PM_Task_Message.objects.filter(
        project__in=activeProjects
    )\
        .filter(
        Q(author=request.user) |
        Q(userTo=request.user) |
        hiddenQ &
        Q(
             unManagedQ
        )
    ).select_related('author', 'project', 'task', 'task__parentTask')
    # result = result.filter(task__active=True)
    options = {
        'OTHER_PROJECTS': True,
        'SYSTEM_MESSAGES': True,
        'USER_MESSAGES': True,
        'COMMIT': True,
    }
    for k in headerValues['COOKIES']:
        if k.startswith('FEED_OPTION_'):
            options[k.replace('FEED_OPTION_', '')] = False if headerValues['COOKIES'][k] == 'N' else True

    opt = 'OTHER_PROJECTS'
    if not options[opt] and headerValues['CURRENT_PROJECT']:
        result = result.filter(project=headerValues['CURRENT_PROJECT'])

    opt = 'SYSTEM_MESSAGES'
    if not options[opt]:
        result = result.exclude(isSystemLog=True)

    opt = 'USER_MESSAGES'
    if not options[opt]:
        result = result.exclude(isSystemLog=False, commit__isnull=True)

    opt = 'COMMITS'
    if not options[opt]:
        result = result.exclude(code='GIT_COMMIT')

    if float(last_id) > 0:
        result = result.filter(id__lt=last_id)

    result = result.order_by('-id')[:20]

    messages = []

    for message in result:
        addParams = {}
        if request.user.get_profile().isManager(message.task.project):
            addParams = {
                'hidden_from_employee': message.hidden_from_employee,
                'hidden_from_clients': message.hidden_from_clients
            }
        messages.append(message.getJson(addParams, request.user))

    templates = templateTools.getMessageTemplates()
    with file(settings.project_root + 'tracker/templates/item_templates/messages/log_message.html') as f:
        templates['template'] = f.read()

    return {
        'messages': messages,
        'templates': templates,
        'options': options
    }