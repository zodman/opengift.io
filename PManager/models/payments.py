__author__ = 'Gvammer'
from django.db import models
from django.contrib.auth.models import User
from PManager.models import PM_Project, PM_Task
from django.db.models.signals import post_save, pre_delete

class Payment(models.Model):
    user = models.ForeignKey(User, related_name='payments', null=True, blank=True)
    payer = models.ForeignKey(User, related_name='repayments', null=True, blank=True)
    project = models.ForeignKey(PM_Project, related_name='payments', null=True, blank=True)
    value = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    class Meta:
        app_label = 'PManager'

class Credit(models.Model):
    user = models.ForeignKey(User, related_name='arrears', null=True, blank=True)
    payer = models.ForeignKey(User, related_name='credits', null=True, blank=True)
    project = models.ForeignKey(PM_Project, related_name='credits', null=True, blank=True)
    value = models.IntegerField()
    task = models.ForeignKey(PM_Task, related_name='costs', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    class Meta:
        app_label = 'PManager'

def payment_account(sender, instance, created, **kwargs):
    if created:
        if instance.user:
            profile = instance.user.get_profile()
            if not profile.account_total: profile.account_total=0
            profile.account_total -= instance.value
            profile.save()
        elif instance.payer:
            profile = instance.payer.get_profile()
            if not profile.account_total: profile.account_total=0
            profile.account_total += instance.value
            profile.save()

def credit_del_account(sender, instance, using, **kwargs):
    payment_account(sender, instance, True)

post_save.connect(payment_account, sender=Payment)
pre_delete.connect(credit_del_account, sender=Credit)

def credit_account(sender, instance, created, **kwargs):
    if created:
        if instance.user:
            profile = instance.user.get_profile()
            if not profile.account_total: profile.account_total=0
            profile.account_total += instance.value
            profile.save()
        elif instance.payer:
            profile = instance.payer.get_profile()
            if not profile.account_total: profile.account_total=0
            profile.account_total -= instance.value
            profile.save()

def payment_del_account(sender, instance, using, **kwargs):
    credit_account(sender, instance, True)

post_save.connect(credit_account, sender=Credit)
pre_delete.connect(payment_del_account, sender=Payment)