# -*- coding:utf-8 -*-
__author__ = 'gvammer'
from django.core.management.base import NoArgsCommand
from django.conf import settings
from django.contrib.auth.models import User
from PManager.models import PM_Reminder
import datetime
from PManager.viewsExt.tools import emailMessage
from django.utils import timezone

def remind(reminder):
    if reminder.task.resp:
        arEmail = [reminder.task.resp.email, 'gvamm3r@gmail.com']
        sendMes = emailMessage('task_reminder',
           {
               'task': reminder.task
           },
           'Вы просили напомнить вам про задачу "' + reminder.task.name + '"'
        )

        try:
            sendMes.send(arEmail)
        except Exception:
            print 'Message doesn\'t send'

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        now = datetime.datetime.now()
        start = datetime.datetime.combine(now, datetime.time.min)
        end = datetime.datetime.combine(now, datetime.time.max)
        reminders = PM_Reminder.objects.filter(date__range=(start, end))
        for reminder in reminders:
            remind(reminder)
