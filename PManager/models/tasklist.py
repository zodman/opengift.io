# -*- coding:utf-8 -*-
__author__ = 'Tonakai'
from django.db import models
from PManager.models.tasks import PM_Project, PM_Task
from PManager.models.users import PM_User
from django.db.models.signals import pre_save
import datetime

class TaskList(models.Model):
    status_choices = (
        (1, u'Открыт'),
        (2, u'Закрыт')
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    project = models.ForeignKey(PM_Project, related_name='task_lists')
    users = models.ManyToManyField(PM_User)
    closed_at = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True, default=1, choices=status_choices)
    def __unicode__(self):
        return "%s#%s" % (self.id, self.project.id)

    class Meta:
        app_label = 'PManager'

def closeTaskList(sender, instance, **kwargs):
    if instance.status == 2:
        instance.closed_at = datetime.datetime.now()

pre_save.connect(closeTaskList, sender=TaskList)