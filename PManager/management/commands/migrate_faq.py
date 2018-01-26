# -*- coding: utf-8 -*-
__author__ = 'gvammer'
from django.core.management.base import NoArgsCommand
from django.conf import settings
from PManager.models import PM_Project, PM_Project_Problem

import datetime
from django.utils import timezone
import warnings, MySQLdb

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        arQuestions = {
            u'': [
                {
                    'name': '',
                    'description': ''
                }
            ]
        }

