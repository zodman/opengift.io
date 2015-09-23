# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from django.db import models
from django.contrib.auth.models import User
from PManager.models.tasks import PM_Tracker, PM_ProjectRoles, PM_Role, PM_Project
from PManager.models.achievements import PM_User_Achievement, PM_Project_Achievement
from PManager.models.payments import Credit
from PManager.viewsExt import headers
from PManager.viewsExt.tools import emailMessage
from django.db.models.signals import post_save, pre_delete
from PManager.customs.storages import path_and_rename
from django.db import connection

class Specialty(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name or ''

    def __unicode__(self):
        return self.name or ''

    class Meta:
        app_label = 'PManager'


def get_random_color():
    import random

    v = random.randint(0, len(PM_User.color_choices) - 1)
    return PM_User.color_choices[v][0]


class PM_User(models.Model):
    color_choices = (
        ('#DA70D6', '#DA70D6'),
        ('#9400D3', '#9400D3'),
        ('#6495ED', '#6495ED'),
        ('#4169E1', '#4169E1'),
        ('#87CEEB', '#87CEEB'),
        ('#008080', '#008080'),
        ('#EEE8AA', '#EEE8AA'),
        ('#F0E68C', '#F0E68C'),
        ('#DCDCDC', '#DCDCDC'),
        ('#708090', '#708090'),
        ('#eed5b7', '#eed5b7'),
        ('#ffdead', '#ffdead'),
        ('#e0eee0', '#e0eee0'),
        ('#836fff', '#836fff'),
        ('#00ee76', '#00ee76'),
        ('#00cd66', '#00cd66'),
        ('#76ee00', '#76ee00'),
        ('#bcee68', '#bcee68'),
        ('#eedc82', '#eedc82'),
        ('#cd5555', '#cd5555'),
        ('#ab82ff', '#ab82ff'),
    )
    user = models.OneToOneField(User, db_index=True, related_name='profile')
    trackers = models.ManyToManyField(PM_Tracker, null=True)
    icq = models.CharField(max_length=70, null=True, blank=True)
    skype = models.CharField(max_length=70, null=True, blank=True)
    birthday = models.DateTimeField(blank=True, null=True)
    avatar = models.ImageField(blank=True, upload_to=path_and_rename("users"))
    sp_price = models.IntegerField(blank=True, null=True, default=0, verbose_name='Ставка')

    premium_till = models.DateTimeField(blank=True, null=True, verbose_name='Оплачен до')
    paid = models.IntegerField(blank=True, null=True, default=0) #todo: deprecated
    specialty = models.ForeignKey(Specialty, blank=True, null=True)  # TODO: deprecated
    specialties = models.ManyToManyField(Specialty, blank=True, null=True, related_name='profiles',
                                         verbose_name='Специальности')
    # all_sp = models.IntegerField(null=True,blank=True)
    avatar_color = models.CharField(blank=True, null=True, default=get_random_color, choices=color_choices,
                                    max_length=20)

    # account_total = models.IntegerField(blank=True, null=True, verbose_name='Счет')
    rating = models.FloatField(blank=True, null=True, verbose_name='Рейтинг', default=0)
    last_activity_date = models.DateTimeField(null=True, blank=True)

    is_outsource = models.BooleanField(blank=True, verbose_name='Аутсорс', default=False)

    @property
    def account_total(self):
        qText = """
                  SELECT
                      sum(value) as summ, user_id FROM pmanager_credit where user_id=""" + str(self.user.id) + """
              """
        cursor = connection.cursor()

        cursor.execute(qText)

        for x in cursor.fetchall():
            if not x[0]:
                continue

            return x[0]
        return 0

    def account_total_project(self, project):
        if not project:
            return 0

        qText = """
                  SELECT
                      sum(value) as summ, user_id FROM pmanager_credit where user_id=""" + str(self.user.id) + """
                      AND project_id=""" + str(project.id) + """
              """
        cursor = connection.cursor()

        cursor.execute(qText)

        for x in cursor.fetchall():
            if not x[0]:
                continue

            return x[0]
        return 0

    @property
    def url(self):
        return "/user_detail/?id=" + str(self.user.id)

    @property
    def avatarSrc(self):
        avatar = str(self.avatar.url) if self.avatar else ''
        if avatar:
            if avatar.find('media') < 0:
                avatar = '/media/' + avatar
        return avatar

    @property
    def avatar_rel(self):
        if self.avatarSrc:
            return {
                'image': self.avatarSrc, 
                'id': self.user.id
            }
        else:
            return {
                'id': self.user.id,
                'color': self.avatar_color,
                'initials': self.user.last_name[0] + self.user.first_name[
                    0] if self.user.last_name and self.user.first_name else ''
            }

    @property
    def managedProjects(self):
        try:
            return PM_Project.objects.filter(pk__in=PM_ProjectRoles.objects.filter(
                user=self.user,
                role=PM_Role.objects.get(code='manager')
            ).values('project__id')).exclude(closed=True, locked=True)
        except PM_Role.DoesNotExist:
            return None

    @staticmethod
    def getCurrent(request):  #возвращает текущего пользователя
        if headers.TRACKER and request.user.is_authenticated():
            return PM_User.getByUser(request.user)

    @staticmethod
    def getByUser(user):
        if headers.TRACKER and user:
            try:
                pm_user = PM_User.objects.get(user=user, trackers=headers.TRACKER)
            except PM_User.DoesNotExist:
                try:
                    pm_user = PM_User.objects.get(user=user)
                except PM_User.DoesNotExist:
                    pm_user = PM_User(user=user)
                    pm_user.save()
                pm_user.trackers.add(headers.TRACKER)

            return pm_user

    @staticmethod
    def getOrCreateByEmail(email, project, role):
        try:
            user = User.objects.filter(username=email).get()  #достанем пользователя по логину
        except User.DoesNotExist:
            password = User.objects.make_random_password()
            login = email
            if len(login) > 30:
                login = login[0:login.find('@')]
            user = User.objects.create_user(login, email, password)
            context = {
                'user_name': ' '.join([user.first_name, user.last_name]),
                'user_login': login,
                'user_password': password
            }

            message = emailMessage('hello_new_user',
                                   context,
                                   'Heliard: сообщество профессионалов. Добро пожаловать!'
            )

            message.send([email])
            # admin
            # todo: Move this method to a service
            from tracker.settings import ADMIN_EMAIL
            message.send([ADMIN_EMAIL])

        if project:
            p_user = PM_User.getByUser(user)
            if not user.is_active:
                user.is_active = True
                user.save()

            p_user.setRole(role, project)

        return user

    def getRating(self, project=None):
        if project:
            if project.getSettings().get('disable_rating', False):
                return 0

            if self.isClient(project):
                return 0

        rate = self.rating or 0
        for uac in PM_User_Achievement.objects.filter(user=self.user, project=project):
            try:
                pac = PM_Project_Achievement.objects.get(
                    project=project,
                    achievement=uac.achievement,
                    type='bet',
                    value__isnull=False
                )
                rate += pac.value

            except PM_Project_Achievement.DoesNotExist:
                continue

        return rate

    def isClient(self, project):
        return self.isRole('client', project)

    def isManager(self, project):
        return self.isRole('manager', project)

    def isEmployee(self, project):
        return self.isRole('employee', project)

    def hasRole(self, project):
        try:
            qs = PM_ProjectRoles.objects.filter(user=self.user, project=project)
            if qs.count() > 0:
                return True
            else:
                return False

        except PM_ProjectRoles.DoesNotExist:
            return False

    def isRole(self, roleCode, project):
        if self.user and project and roleCode:
            try:
                clientRole = PM_Role.objects.get(code=roleCode)
                try:
                    userRole = PM_ProjectRoles.objects.filter(user=self.user, role=clientRole, project=project)
                    if userRole and userRole[0]:
                        return True
                except PM_ProjectRoles.DoesNotExist:
                    pass
            except PM_Role.DoesNotExist:
                pass

        return False

    def setRole(self, roleCode, project, type=None):
        if self.user and project and roleCode:
            try:
                clientRole = PM_Role.objects.get(code=roleCode, tracker=headers.TRACKER)
            except PM_Role.DoesNotExist:
                return False

            if clientRole:
                userRole, created = PM_ProjectRoles.objects.get_or_create(user=self.user, role=clientRole,
                                                                          project=project)
                if type:
                    userRole.payment_type = type
                    userRole.save()
        return self

    def getProjects(self, only_managed=False, locked=False):
        userRoles = PM_ProjectRoles.objects.filter(user=self.user)
        if only_managed:
            userRoles = userRoles.filter(role__code='manager')

        arId = [role.project.id for role in userRoles]
        projects = PM_Project.objects.filter(id__in=arId, closed=False)
        if not locked:
            projects = projects.filter(locked=False)
        projects = projects.distinct()
        return projects

    def getRoles(self, project):
        return [r.role for r in PM_ProjectRoles.objects.filter(user=self.user, project=project)]

    def getProjectUsers(self, project):
        return project.getUsers()

    def deleteRole(self, role, project):
        if self.user:
            userRole = PM_ProjectRoles.objects.get(user=self.user, role__code=role, project=project)
            if userRole:
                userRole.delete()

        return self

    def hasAccess(self, task, rule):
        if task and hasattr(task, 'project') and task.project:
            if self.isManager(task.project):
                return True

            if task.author.id == self.user.id:
                return True

            if rule == 'view':
                if task.onPlanning and not task.resp:
                    return self.hasRole(task.project)

                return (task.resp and self.user.id == task.resp.id) \
                       or self.user.id in [u.id for u in task.observers.all()] \
                       or task.subTasks.filter(resp=self.user.id, active=True).count() > 0 \
                       or task.subTasks.filter(author=self.user.id, active=True).count() > 0

            elif rule == 'change':
                #todo: разделить по конкретным изменениям
                # (разработчики могут только принимать задачи без ответственного)
                return self.isEmployee(task.project) and not task.resp \
                       or self.user.id == task.resp

    def getBet(self, project, type=None, role_code=None):
        try:
            projectRole = PM_ProjectRoles.objects.filter(user=self.user, project=project)

            if type:
                projectRole = projectRole.filter(payment_type=type)

            if role_code:
                projectRole = projectRole.filter(role__code=role_code)

            rate = 0

            if projectRole:
                projectRole = projectRole[0]

                rate = projectRole.rate if projectRole.rate is not None else (
                    int(self.sp_price) if self.sp_price else 0)

                if rate:
                    rate += self.getRating(project)

            return rate

        except PM_ProjectRoles.DoesNotExist:
            return 0

    def getPaymentType(self, project, roleCode=False):
        for role in PM_ProjectRoles.objects.filter(user=self.user, project=project):
            if role.payment_type and (not roleCode or roleCode == role.role.code):
                return role.payment_type

        return 'real_time'

    def __str__(self):
        return "%s's profile" % self.user

    class Meta:
        app_label = 'PManager'


def remove_keys(sender, instance, **kwargs):
    from tracker.settings import USE_GIT_MODULE
    from PManager.classes.git.gitolite_manager import GitoliteManager
    from PManager.models.keys import Key

    keys = Key.objects.filter(user=instance)
    for key in keys:
        GitoliteManager.remove_key_from_user(key, instance)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = PM_User.objects.get_or_create(user=instance)


pre_delete.connect(remove_keys, sender=User)
post_save.connect(create_user_profile, sender=User)
