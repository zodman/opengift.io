__author__ = 'gvammer'
from django.core.management.base import NoArgsCommand
from django.contrib.auth.admin import User
from PManager.models import PM_User
import datetime
from django.utils import timezone
from PManager.viewsExt.tools import templateTools

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        """
        :param options:
        :return:
        """
        for u in PM_User.objects.filter(blockchain_wallet__isnull=False):
            u.update_opengifter_level()