# -*- coding:utf-8 -*-
from django.db import DatabaseError

__author__ = 'Rayleigh'
from PManager.models.tasks import PM_Tracker

def get_tracker(prim_key=1):
    return PM_Tracker.objects.get(pk=prim_key)
