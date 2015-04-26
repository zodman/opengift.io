from django.db.models import Q

__author__ = 'rayleigh'

from PManager.models import TaskDraft

# todo implement this
def create_tasklist_from_project(project):
    # should get tasks which can be outsourced
    pass


def draft_cnt(user):
    try:
        cnt = TaskDraft.objects.filter(
            Q(users__id=user.id, _status=TaskDraft.OPEN) |
            Q(author=user.id, closed_at__isnull=True)).count()
    except TaskDraft.DoesNotExist:
        cnt = 0
    return cnt