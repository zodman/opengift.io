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
        warnings.filterwarnings('error', category=MySQLdb.Warning)
        for p in PM_Project.objects.filter(description__isnull=False):
            if p.target_group and p.problem:
                n = PM_Project_Problem(target_group=p.target_group, problem=p.problem, solution=p.description)
                try:
                    n.save()
                    print n
                    p.problems.add(n)
                except MySQLdb.Warning:
                    pass
                except ValueError, Warning:
                    pass

