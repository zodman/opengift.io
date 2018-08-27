# -*- coding:utf-8 -*-
__author__ = 'gvammer'
from django.core.management.base import NoArgsCommand
from django.conf import settings
from django.contrib.auth.models import User
from PManager.models import PM_User, PM_Project
from PManager.services.docker import blockchain_user_register_request, blockchain_user_getkey_request, blockchain_user_newproject_request


class Command(NoArgsCommand):
    def handle_noargs(self, **options):

        projects = PM_Project.objects.filter(
            blockchain_name__isnull=False,
            blockchain_registered=False
        )

        for p in projects:
            uProf = p.author.get_profile()
            if not uProf.blockchain_wallet:
                result = blockchain_user_register_request(uProf.user.username)
                print result
                if result.find('Error') == -1:
                    res = result.split("\n\n")
                    uProf.blockchain_key = res[0]
                    uProf.blockchain_cert = res[1]
                    wallet = blockchain_user_getkey_request(uProf.user.username)
                    print wallet
                    uProf.blockchain_wallet = wallet
                    uProf.save()

            res = blockchain_user_newproject_request(p.author.username, p.blockchain_name)
            print res
            if res == 'ok':
                p.blockchain_registered = True
                p.save()
