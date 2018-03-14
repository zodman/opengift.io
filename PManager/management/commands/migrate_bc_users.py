# -*- coding: utf-8 -*-
__author__ = 'gvammer'
from django.core.management.base import NoArgsCommand
from django.conf import settings
from PManager.models import PM_User, PM_Project
from django.contrib.auth.models import User
from PManager.services.docker import blockchain_user_register_request, blockchain_user_getkey_request, blockchain_user_newproject_request


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        u = PM_User.objects.filter(blockchain_wallet__isnull=False)

        for us in u:
            result = blockchain_user_register_request(us.user.username)
            if result.find('Error') == -1:
                res = result.split("\n\n")
                us.blockchain_key = res[0]
                us.blockchain_cert = res[1]
                us.blockchain_wallet = blockchain_user_getkey_request(us.user.username)
                us.save()
                print us.blockchain_wallet
                p = PM_Project.objects.filter(author=us.user, blockchain_name__isnull=False)
                for pr in p:
                    blockchain_user_newproject_request(us.user.username, pr.blockchain_name)
                    print pr.blockchain_name




