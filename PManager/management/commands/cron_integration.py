# -*- coding: utf-8 -*-
__author__ = 'gvammer'
from django.core.management.base import NoArgsCommand
from django.conf import settings
from PManager.models import PM_Task, SlackIntegration
import datetime
from django.utils import timezone


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        for integration in SlackIntegration.objects.all():
            now = datetime.datetime.now()
            tasks = PM_Task.objects.filter(project=integration.project)
            if integration.lastSendDate:
                tasks = tasks.filter(dateClose__gt=integration.lastSendDate)
            else:
                tasks = tasks.filter(dateClose__gt=(now - datetime.timedelta(days=1)))

            for task in tasks:
                integration.send({'text': u'Задача <https://heliard.ru' + task.url + u'|' + task.name + u'> закрыта.'})

            integration.lastSendDate = now
            integration.save()
