from django.db.models import Q

__author__ = 'rayleigh'

from PManager.models import TaskDraft
from django.contrib.auth.models import User

# todo implement this
def create_tasklist_from_project(project):
    # should get tasks which can be outsourced
    pass


def draft_cnt(user):
    try:
        cnt = drafts(user).count()
    except TaskDraft.DoesNotExist:
        cnt = 0
    return cnt


def task_draft_is_user_participate(task_id, user_id, author_id):
    try:
        drafts_cnt = TaskDraft.objects.filter(tasks__id=task_id, author__id=author_id, users__id=user_id).count()
    except TaskDraft.DoesNotExist:
        return False
    if draft_cnt > 0:
        return User.objects.get(pk=user_id)
    return False


def get_draft_by_id(draft_id, user):
    try:
        draft = TaskDraft.objects.get(pk=int(draft_id), users__id=user.id, deleted=False)
        return draft
    except (ValueError, TaskDraft.DoesNotExist):
        return False


def get_draft_by_slug(slug, user):
    try:
        draft = TaskDraft.objects.get(slug=slug, users__id=user.id, deleted=False)
        return draft
    except (ValueError, TaskDraft.DoesNotExist):
        return False


def drafts(user):
    query = TaskDraft.objects.filter(
        Q(users__id=user.id, _status=TaskDraft.OPEN) |
        Q(author=user.id, closed_at__isnull=True)).filter(deleted=False)
    return query


def get_unique_slug():
    slug = __slug()
    while TaskDraft.objects.filter(slug=slug).count() > 0:
        slug = __slug()
    return slug


def __slug(length=64):
    import random
    import string
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(length)])

