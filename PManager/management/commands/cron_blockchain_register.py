# -*- coding:utf-8 -*-
__author__ = 'gvammer'
from django.core.management.base import NoArgsCommand
from django.conf import settings
from django.contrib.auth.models import User
from PManager.models import PM_User, PM_Project
from PManager.services.docker import blockchain_user_register_request, blockchain_user_getkey_request, blockchain_user_newproject_request


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        newUsers = PM_User.objects.filter(is_bc_user=True)
        arUsers = []
        for uProf in newUsers:
            arUsers.append(uProf.user.id)
            result = blockchain_user_register_request(uProf.user.username)
            if result.find('Error') == -1:
                res = result.split("\n\n")
                uProf.blockchain_key = res[0]
                uProf.blockchain_cert = res[1]
                uProf.blockchain_wallet = blockchain_user_getkey_request(uProf.user.username)
                uProf.save()

        projects = PM_Project.objects.filter(
            blockchain_name__isnull=False,
            blockchain_registered=False,
            author__in=arUsers
        )
