__author__ = 'Gvammer'
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from PManager.models.tasks import PM_Task
from django.db.models.signals import pre_save
from django.dispatch import receiver

class PM_Achievement(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="PManager/static/upload/achievement/", null=True)
    description = models.TextField()
    condition = models.TextField()
    code = models.CharField(max_length=100)

    @property
    def smallImageUrl(self):
        return str(self.image).replace('PManager', '')

    def addToUser(self, user):
        acc, created = PM_User_Achievement.objects.get_or_create(user=user, achievement=self)
        acc.save()

    def checkForUser(self, user):
        challenges = PM_Achievement.objects.exclude(
            id__in=PM_User_Achievement.objects.filter(user=user).values('achievement__id')
        )
        for achievement in challenges:
            pass

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'PManager'

@receiver(pre_save, sender=PM_Task)
def addAchievement(sender, instance, **kwargs):
    if instance.id:
        oldTask = PM_Task.objects.get(pk=instance.id)
        if instance.closed and \
            instance.resp and \
                instance.resp.id != instance.author.id and \
                not oldTask.wasClosed:

            acc = PM_Achievement.objects.get(code='first_closed_task')
            if (acc.addToUser(instance.resp)):
                prof = instance.resp.get_profile()
                rating = prof.rating or 0
                prof.rating = rating + 10
                prof.save()


class PM_User_Achievement(models.Model):
    user = models.ForeignKey(User, related_name='user_achievements')
    achievement = models.ForeignKey(PM_Achievement)
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(blank=True, default=False)

    class Meta:
        app_label = 'PManager'

class AchievementEvents(models.Model):
    name = models.CharField(max_length=255)

class ControllerDataType(models.Model):
    name = models.CharField(max_length=255)

class DataController(models.Model):
    dataType = models.ForeignKey(ControllerDataType)
    value = models.FloatField()
    user = models.ForeignKey(User)
    date = models.DateTimeField(default=datetime.now())

class Checker(models.Model):
    dataType = models.ForeignKey(ControllerDataType)

    conditionType = models.CharField(max_length=255)
    condition = models.CharField(max_length=2)
    conditionElem = models.FloatField(blank=True,null=True)
    otherCondition = models.CharField(max_length=255)

    dateTimeStart = models.DateTimeField(blank=True,null=True)
    dateTimeEnd = models.DateTimeField(blank=True,null=True)

    def check(self,user):
        otherData = None
        if self.otherCondition == 'otherUsers':
            otherData = DataController.objects.filter(dataType=self.dataType,user=user)
        else:
            pass

        data = DataController.objects.filter(dataType=self.dataType,user=user,date__gt=self.dateTimeStart,date__lt=self.dateTimeEnd)

        compareElem = self.conditionElem
        if self.conditionType == 'sum':
            sum, compareElem = 0,0

            for elem in data:
                sum += elem.value

            if otherData:
                for elem in otherData:
                    compareElem += elem.value

        return_el = 0
        str = 'return_el = compareData%s%s' % self.condition, compareElem
        exec str

        return return_el

class Trigger(models.Model):
    name = models.CharField(max_length=255)
    checker = models.ManyToManyField(Checker)
    arEvents = models.ManyToManyField(AchievementEvents)
    permanent = models.BooleanField(default=False)

    def check(self,user):
        return self.checker.check(user)
