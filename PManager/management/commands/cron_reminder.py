__author__ = 'gvammer'
from django.core.management.base import NoArgsCommand
from django.conf import settings
from django.contrib.auth.models import User
from PManager.models import PM_Reminder
import datetime
from django.utils import timezone

def remind(reminder):
    print reminder

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        now = datetime.datetime.now()
        start = datetime.datetime.combine(now, datetime.time.min)
        end = datetime.datetime.combine(now, datetime.time.max)
        reminders = PM_Reminder.objects.filter(datetime__range=(start, end))
        for reminder in reminders:
            remind(reminder)
