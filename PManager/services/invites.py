# -*- coding:utf-8 -*-
from django.db.models import Q, F

__author__ = 'Tonakai'
from PManager.services.activity import last_project_activity
from PManager.models.tasks import PM_Task, PM_Milestone
from datetime import timedelta
from django.utils import timezone

# should return true if no activity on the project and we can
# invite devs to close projects tasks
# todo implement this


def should_suggest_outsource(project):
    return is_project_failing(project) or is_project_stale(project)


def is_project_stale(project):
    return timezone.now() - timedelta(days=5) > last_project_activity(project)


# should return true if hours in tasks more than left in milestone
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


# return users that can take tasks from tasks_list
def executors_available(tasklist):
    from PManager.services.rating import get_top_users
    user_ids = set()
    for task in tasklist.tasks.all():
        for user_id, weight in get_top_users(task):
            user_ids.add(user_id)

    # we have users that qualify, so now we need to get those, who available? no
    # we need to sort before/ what to do if task has no available users?
    # already request in iteration, which is baaaaad
    return users

# what i should do
# 1. should system suggest outsource (condition)
# 2. grab tasks from project to form a tasklist
# 3. suggest tasklist to manager for approval
# 4. after approval attach discussion to tasklist
# 5. choose developers that are capable of doing that stuff
# 6. send tasklist to all developers (email)
# 7. add link to tasklist/suggestion to user/manager homepage
# 8. show new messages count in tasklist
# 9. easy choose and assign user to task
# 10. complete
#

# condition -> create -> show to manager |
# (event) manager_task_approve|
# -> send invites -> share tasks -> create discussion board |
# (event) discussing details|
# -> approve executor|
# -> add user to project -> assign tasks
# ----if tasklist not closed by empty | can be issued to add users to it
# /****
# if should_suggest_outsource(project):
# tasklist = create_task_list(project)
# sendForApproval(manager, tasklist)
#     *****/ -> thats cron functions
# #
# Edit_tasklist | Delete_tasklist | Create_tasklist (some of this)
# def approve_tasklist_action(tasklist, manager):
#     users = get_users_to_invite()
#     tasklist.discussion = new discussion()
#     grantAccess(users, tasklist)
#     sendInvites(users, tasklist)
# #
# Add | Edit | Delete Comments on discussion board
# def assingTaskTo(users, task, tasklist):
#     assign___
#     message = tasklist.get_discussion(task)
#     task.addMessage(message)
#     tasklist.remove(task)
# #
# event| on tasklist.CLOSED -> (all tasks)
# tasklist.close()
#
#
