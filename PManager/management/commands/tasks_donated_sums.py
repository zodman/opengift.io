# -*- coding:utf-8 -*-
__author__ = 'gvammer'
from django.core.management.base import NoArgsCommand
from django.conf import settings
from django.contrib.auth.models import User
from PManager.viewsExt.crypto import get_paid_btc
from PManager.models import PM_Task
from tracker.settings import GIFT_USD_RATE

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        for p in PM_Task.objects.filter():
            p.donate_sum = p.donated / GIFT_USD_RATE
            p.save()