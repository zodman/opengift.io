# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from django.db import models
from django.contrib.auth.models import User
from PManager.models.tasks import PM_Task, PM_Project
from PManager.models.payments import Credit
from django.db.models.signals import pre_save
from django.dispatch import receiver

class PM_Achievement(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="tracker/media/achievement/", null=True)
    description = models.TextField()
    condition = models.TextField()
    code = models.CharField(max_length=100)
    delete_on_first_view = models.BooleanField(blank=True)
    use_in_projects = models.BooleanField(blank=True)

    @property
    def smallImageUrl(self):
        return str(self.image).replace('tracker', '')

    def projectSettingsForAchievement(self, project):
        try:
            return PM_Project_Achievement.objects.get(project=project, achievement=self)
        except PM_Project_Achievement.DoesNotExist:
            return None

    def addToUser(self, user, project=None):
        """
        :param user:  instance of User
        :param project: instance of PM_Project
        :return: Boolean
        """
        can_add_achievement, ps = False, None
        if project:
            ps = self.projectSettingsForAchievement(project)
            if ps:
                can_add_achievement = True
        else:
            can_add_achievement = True

        created = False
        if can_add_achievement:
            acc, created = PM_User_Achievement.objects.get_or_create(user=user, achievement=self)
            if project:
                acc.project = project
                acc.save()

            if created:
                if ps:
                    if ps.value:
                        if ps.type == 'fix':
                            credit = Credit(user=user, value=ps.value, project=project, type='achievement ' + str(self.id))
                            credit.save()

        return created

    def checkForUser(self, user, project=None):
        """
        :param user: instance of User
        :param project: instance of PM_Project
        :return: Boolean
        """
        ua = PM_User_Achievement.objects.filter(achievement=self, user=user)
        if project:
            ua = ua.filter(project=project)

        return not ua.exists()

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'PManager'

class PM_Project_Achievement(models.Model):
    type_choice = (
        ('fix', u'Фиксированное начисление'),
        ('bet', u'Увеличение ставки по проекту'),
    )

    achievement = models.ForeignKey(PM_Achievement)
    project = models.ForeignKey(PM_Project)
    value = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=100, choices=type_choice, default='fix')
    once_per_project = models.BooleanField()

    class Meta:
        app_label = 'PManager'

@receiver(pre_save, sender=PM_Task)
def addAchievement(sender, instance, **kwargs):
    if instance.id:
        try:
            oldTask = PM_Task.objects.get(pk=instance.id)
            if instance.closed and \
                instance.resp and \
                    instance.resp.id != instance.author.id and \
                    not oldTask.wasClosed:

                acc = PM_Achievement.objects.get(code='first_closed_task')
                acc.addToUser(instance.resp, instance.project)

        except PM_Achievement.DoesNotExist:
            pass

class PM_User_Achievement(models.Model):
    user = models.ForeignKey(User, related_name='user_achievements')
    achievement = models.ForeignKey(PM_Achievement, related_name='achievement_users')
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(blank=True, default=False)
    text = models.CharField(max_length=400, blank=True, null=True)
    project = models.ForeignKey(PM_Project, null=True)

    class Meta:
        app_label = 'PManager'