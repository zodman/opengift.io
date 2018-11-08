# -*- coding:utf-8 -*-
from django.db import DatabaseError
from django.utils.functional import lazy
from PManager.models.tasks import PM_Tracker
__author__ = 'Rayleigh'

@lazy
def get_tracker(prim_key=1):
    return PM_Tracker.objects.get(pk=prim_key)
