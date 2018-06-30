# -*- coding:utf-8 -*-
__author__ = 'gvammer'
from django.core.management.base import NoArgsCommand
from django.conf import settings
from django.contrib.auth.models import User
from PManager.models import PM_Project
from PManager.viewsExt.tools import emailMessage

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        projects = PM_Project.objects.filter(public=True)
        for p in projects:

            message = emailMessage(
                'custom',
                {
                    'first_name': p.author.first_name,
                    'last_name': p.author.last_name
                },
                'Just take our GIFTs!'
            )

            message.send([p.author.email])
