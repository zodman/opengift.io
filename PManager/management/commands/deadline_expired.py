
__author__ = 'zodman'
from django.core.management.base import NoArgsCommand
from django.utils import timezone
from django.contrib.auth.models import User
from PManager.models import PM_Task

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        now = timezone.now()
        # TODO: Create user: robot_checker
        user = User.objects.get(username="admin")
        tasks = PM_Task.objects.exclude(deadline__isnull=True)
        for task in tasks:
            if task.deadline > now:
                task.Close(user=user)
                text_desc = "Task id %s  was close because deadline expire" % task.id    
                task.systemMessage(text=text_desc,user=user,code="DEADLINE_EXPIRED")
