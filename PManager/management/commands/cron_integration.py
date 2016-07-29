# -*- coding: utf-8 -*-
__author__ = 'gvammer'
from django.core.management.base import NoArgsCommand
from django.conf import settings
from PManager.models import PM_Task, SlackIntegration, PM_Task_Message

import datetime
from django.utils import timezone


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        for integration in SlackIntegration.objects.all():
            now = datetime.datetime.now()
            dateGt = integration.lastSendDate if integration.lastSendDate else now - datetime.timedelta(days=1)

            for message in PM_Task_Message.objects.filter(
                    project=integration.project,
                    code__in=['STATUS_READY', 'STATUS_REVISION', 'TASK_CREATE' , 'TASK_CLOSE'],
                    dateCreate__gt=dateGt
            ):
                integration.send({'text': u'<https://heliard.ru' + message.task.url + u'|' + message.task.name + u'> ' + message.text})

            integration.lastSendDate = now
            integration.save()
