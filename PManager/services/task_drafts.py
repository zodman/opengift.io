__author__ = 'rayleigh'
from django.db.models import Q
from PManager.models import TaskDraft, PM_Task
from django.contrib.auth.models import User
from PManager.models.simple_message import SimpleMessage
from PManager.models import PM_Task_Message, PM_ProjectRoles


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
        Q(author=user.id, closed_at__isnull=True)).filter(deleted=False).distinct()
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


def draft_simple_msg_cnt(task, draft):
    try:
        cnt = SimpleMessage.objects.filter(task=task, task_draft=draft).count()
        return cnt
    except (ValueError, SimpleMessage.DoesNotExist):
        return 0


def accept_user(draft, task_id, user_accepted_id, cur_user):
    from tracker.settings import USE_GIT_MODULE
    if not cur_user.id == draft.author.id:
        return False
    try:
        task = PM_Task.objects.get(pk=int(task_id))
        user = User.objects.get(pk=int(user_accepted_id))
    except (ValueError, PM_Task.DoesNotExist, User.DoesNotExist):
        return False
    if task.resp is not None:
        return False
    try:
        already_in_project = PM_ProjectRoles.objects.filter(user=user, project=task.project).count() > 0
    except PM_ProjectRoles.DoesNotExist:
        already_in_project = False
    if not already_in_project:
        user.get_profile().setRole("employee", task.project)
        if USE_GIT_MODULE:
            from PManager.classes.git.gitolite_manager import GitoliteManager
            GitoliteManager.regenerate_access(task.project)
    task.resp = user
    task.save()
    __create_message_from_simple_messages(draft, task, cur_user, user)
    return True


def __create_message_from_simple_messages(draft, task, author, recipient):
    text = ""
    compile_messages = SimpleMessage.objects.filter(task_draft=draft, task=task)
    for cm in compile_messages:
        text += "<div>"
        text += "<span class='user'>%s</span>:&nbsp;" % cm.author
        text += "<span class='message'>%s</span>" % cm.text
        text += "</div>"
    message = PM_Task_Message.objects.create(text=text, author=author,
                                             userTo=recipient, isSystemLog=True, code='COMPILE_OUTSOURCE')
    message.save()






