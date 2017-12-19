# -*- coding:utf-8 -*-
__author__ = 'gvammer'
from django.core.management.base import NoArgsCommand
from django.conf import settings
from django.contrib.auth.models import User
from PManager.viewsExt.crypto import get_paid_btc


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        print get_paid_btc()
