# -*- coding:utf-8 -*-
__author__ = 'Tonakai'
from django.db import models
from PManager.models.tasks import PM_Project, PM_Task
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
import datetime


class TaskList(models.Model):
    OPEN = 1
    CLOSED = 0
    status_choices = (
        (OPEN, u'Открыт'),
        (CLOSED, u'Закрыт')
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    project = models.ForeignKey(PM_Project, related_name='task_lists')
    users = models.ManyToManyField(User)
    tasks = models.ManyToManyField(PM_Task)
    closed_at = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True, default=CLOSED, choices=status_choices)

    def __unicode__(self):
        return "%s#%s" % (self.id, self.project.id)

    class Meta:
        app_label = 'PManager'


def close_task_list(sender, instance, **kwargs):
    if instance.pk is None:
        instance.status = TaskList.CLOSED
        instance.closed_at = None
        return
    if instance.status == TaskList.CLOSED \
            and instance.closed_at is None:
        old = TaskList.objects.get(pk=instance.id)
        if old.status != instance.status:
            instance.closed_at = datetime.datetime.now()
        return
    if instance.status == TaskList.OPEN \
            and (instance.tasks is None
                 or instance.users is None):
        instance.status == TaskList.CLOSED
        return


pre_save.connect(close_task_list, sender=TaskList)