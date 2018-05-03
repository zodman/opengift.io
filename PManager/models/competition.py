# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from django.db import models
from PManager.models import PM_Task

class Competition(models.Model):
    tasks = models.ManyToManyField(PM_Task)
    dateCreate = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'PManager'