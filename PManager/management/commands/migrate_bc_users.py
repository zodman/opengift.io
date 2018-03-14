# -*- coding: utf-8 -*-
__author__ = 'gvammer'
from django.core.management.base import NoArgsCommand
from django.conf import settings
from PManager.models import PM_User
from django.contrib.auth.models import User
from PManager.services.docker import blockchain_user_register_request, blockchain_user_getkey_request


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        u = PM_User.objects.filter(blockchain_wallet__isnull=False)

        for us in u:
            result = blockchain_user_register_request(us.user.email)
            if result.find('Error') == -1:
                res = result.split("\n\n")
                us.blockchain_key = res[0]
                us.blockchain_cert = res[1]
                us.blockchain_wallet = blockchain_user_getkey_request(us.user.email)
                us.save()
                print us.blockchain_wallet


