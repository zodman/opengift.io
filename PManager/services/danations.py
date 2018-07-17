# -*- coding:utf-8 -*-
__author__ = 'rayleigh'
from PManager.models.tasks import PM_Project_Donation, PM_Task_Message
from django.contrib.auth.models import User


def donate(sum, project, user=None, milestone=None, exchangeUser=None, refUser=None, task=None):
    from PManager.services.docker import blockchain_donate_request

    if not project.blockchain_name:
        return False

    # if user and user.is_authenticated() and user.get_profile().hasRole(project):
    #     return False

    milestoneCode = None
    if milestone:
        milestoneCode = 'opengift.io:' + str(milestone.id)
        milestone.is_request = False
        milestone.save()

    if task:
        milestoneCode = 'opengift.io:task-' + str(task.id)

    res = blockchain_donate_request(
        exchangeUser if exchangeUser else user.username,
        project.blockchain_name,
        sum,
        milestoneCode
    )

    if res == 'ok':
        if exchangeUser:
            try:
                exchangeUser = User.objects.get(username=exchangeUser)
            except User.DoesNotExist:
                pass

        donation = PM_Project_Donation(
            user=user,
            project=project,
            sum=sum,
            milestone=milestone,
            task=task,
            exchange=exchangeUser,
            ref=refUser
        )
        donation.save()

        message = PM_Task_Message(
            author=user,
            project=project,
            task=task,
            code='DONATION',
            donated=sum,
            text='Donated ' + str(sum) + ' GIFTs'
        )
        message.save()

        if task:
            ar_email = task.getUsersEmail()
            from PManager.viewsExt.tools import emailMessage
            import datetime
            from django.utils import timezone

            task.donate_exists = True
            task.save()

            task_data = {
                'task_url': task.url,
                'name': task.project.name + '. ' + task.name,
                'dateCreate': timezone.make_aware(datetime.datetime.now(), timezone.get_current_timezone())
            }

            mail_sender = emailMessage(
                'new_donation_received',
                {
                    'task': task_data,
                    'sum': sum,
                    'donator': {
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                    }
                },
                u'New donation: ' + task_data['name'] + '!'
            )

            try:
                mail_sender.send(ar_email)
            except Exception:
                print 'Email has not sent'

        return True

    return False
