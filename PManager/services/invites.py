# -*- coding:utf-8 -*-
from PManager.viewsExt.tools import emailMessage

__author__ = 'Rayleigh'
from PManager.services.activity import last_project_activity, user_active_tasks
from PManager.models.tasks import PM_Task, PM_Milestone, PM_Task_Message, PM_User_PlanTime
from datetime import timedelta, datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Q, F
from PManager.services.rating import get_top_users
from PManager.models.users import PM_User
from tracker.settings import ADMIN_EMAIL


def should_suggest_outsource(project):
    return is_project_failing(project) or is_project_stale(project)


def is_project_stale(project):
    return timezone.now() - timedelta(days=5) > last_project_activity(project)


def is_project_failing(project):
    return has_dead_milestones(project) or has_dead_tasks(project)


def has_dead_tasks(project):
    HOURS_IN_DAY_NORMAL = 4  # suggesting hours a day value
    try:
        where = ["planTime >= (TIMESTAMPDIFF(DAY, NOW(), deadline) * %s) or deadline < NOW()"]
        tasks = PM_Task.objects.filter(project=project, closed=False, active=True).extra(where=where, params=[str(HOURS_IN_DAY_NORMAL)])
        return tasks.count() > 0
    except PM_Task.DoesNotExist:
        return False

def has_dead_milestones(project):
    try:
        milestones = PM_Milestone.objects.filter(project=project, overdue=True, closed=False)
        return milestones.count() > 0
    except PM_Milestone.DoesNotExist:
        return False


def get_evaluations(user, draft, task):
    if not user:
        return None
    if not draft:
        return None
    if not task:
        return None
    try:
        if user.id == draft.author.id:
            evaluations = PM_User_PlanTime.objects.filter(user__in=draft.users.distinct(), task=task)
        else:
            evaluations = PM_User_PlanTime.objects.filter(user=user, task=task)
        return evaluations
    except (ValueError, PM_Task_Message.DoesNotExist):
        return None

def get_all_active_outsourcers(time_inactive=30, exclude=None, specialties=[]):
    last_date = datetime.now() - timedelta(days=time_inactive)
    user_ids = PM_User.objects.filter(
                                   is_outsource=True,
                                   user__is_active=True,
                                   last_activity_date__gt=last_date,
                                   last_activity_date__isnull=False)
    if specialties:
        user_ids = user_ids.filter(specialties__in=specialties)

    user_ids = user_ids.values_list('user_id', flat=True)
    if user_ids:
        users = User.objects.filter(pk__in=user_ids)
        if exclude is not None:
            for x in exclude:
                users = users.exclude(pk__in=x)
        return users
    else:
        return False

def executors_available(task_draft, active_task_limit=5):
    NUMBER_OF_TOP_USERS = 6
    user_ids = set()
    users = get_all_active_outsourcers(exclude=(task_draft.users.values_list('id', flat=True),), specialties=task_draft.specialties.all())
    if not users:
        return None

    for task in task_draft.tasks.all():
        task_users = users.exclude(pk__in=task.project.getUsers().values_list('id', flat=True)).distinct()
        if task_users:
            for user_id, weight in get_top_users(task=task, limit=NUMBER_OF_TOP_USERS, user_filter=task_users).iteritems():
                try:
                    user_ids.add(int(user_id))
                except ValueError:
                    continue

    if not user_ids:
        user_ids = users.values_list('id', flat=True)

    users_acceptable = set()
    for user_id in user_ids:
        if user_active_tasks(user_id) < active_task_limit:
            users_acceptable.add(user_id)

    return users_acceptable


def send_invites(users, draft):
    sender = emailMessage(
        'invite_draft',
        {
            'draft': draft,
            'tasks': draft.tasks.all()
        },
        'Приглашение к сотрудничеству'
    )
    sender.send([ADMIN_EMAIL])
    for user in users:
        sender.send([user.user.email])
