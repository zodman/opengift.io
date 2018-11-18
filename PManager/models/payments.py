# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from django.db import models
from django.contrib.auth.models import User
from PManager.models import PM_Project, PM_Task
from django.db.models.signals import post_save, pre_delete
from django.db import connection


class Credit(models.Model):
    user = models.ForeignKey(User, related_name='arrears', null=True, blank=True)
    payer = models.ForeignKey(User, related_name='credits', null=True, blank=True)
    project = models.ForeignKey(PM_Project, related_name='credits', null=True, blank=True)
    value = models.IntegerField()
    task = models.ForeignKey(PM_Task, related_name='costs', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)

    @staticmethod
    def getUsersDebt(projects=None):
        table_name = Credit.objects.model._meta.db_table
        if  not projects:
            projects = []
            qText = """ 
            SELECT   sum(value) as summ, user_id 
            FROM {} GROUP BY user_id
              """.format(table_name)    
        else:
            qText = """
                    SELECT
                        sum(value) as summ, user_id FROM {} where project_id in (%s) GROUP BY user_id
                """.format(table_name)
        cursor = connection.cursor()

        args = [ ','.join([str(s.id) for s in projects])]
        cursor.execute(qText, args)
        arElems = []
        for x in cursor.fetchall():
            if not x[1]:
                continue

            arElems.append({
                'sum': x[0],
                'user_id': x[1]
            })

        return arElems

    class Meta:
        app_label = 'PManager'

class PaymentRequest(models.Model):
    user = models.ForeignKey(User, related_name='payment_requests', null=True, blank=True)
    project = models.ForeignKey(PM_Project, related_name='payment_requests', null=True, blank=True)
    value = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        app_label = 'PManager'

class Fee(models.Model):
    user = models.ForeignKey(User, related_name='fee', null=True, blank=True)
    project = models.ForeignKey(PM_Project, related_name='fee', null=True, blank=True)
    value = models.IntegerField()
    task = models.ForeignKey(PM_Task, related_name='fee', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    type = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        app_label = 'PManager'