# -*- coding:utf-8 -*-
__author__ = 'Tonakai'
from django.contrib.auth.models import User
from PManager.models.tasks import PM_Project
from PManager.models.tasks import PM_Timer
from tracker.settings import GIT_PUSH_MESSAGE
import logging
logger = logging.getLogger(__name__)


class Warden(object):
    user = None
    project = None
    timer = None

    def __init__(self, username, repository):
        self.user = self.get_user(username)
        self.project = self.get_project(repository)
        if self.user is None or self.project is None:
            raise AssertionError("Cant use empty user or project")

    def close_task(self):
        if self.is_task() == 'true' and self.timer:
            logger.info(u'Set ready at active task {0:s} for user {1:s}'.format(self.timer.task, self.user))
            self.timer.task.endTimer(user=self.user, comment=GIT_PUSH_MESSAGE)
            self.timer.task.setStatus(status='ready')
            return 'true'
        logger.info(u'Active task not found for user {0:s}'.format(self.user))
        return 'false'

    def is_task(self):
        try:
            timer = PM_Timer.objects.get(user=self.user, dateEnd__isnull=True)
            logger.info(u'Active timer found. User: {0:s} Project: {1:s}'.format(self.user, self.project))
        except PM_Timer.DoesNotExist:
            logger.info(u'Active timer not found. User: {0:s} Project: {1:s}'.format(self.user, self.project))
            timer = None
        if timer and timer.task.project == self.project:
            self.timer = timer
            return 'true'
        return 'false'

    def write_message(self, ref, hashes):

        pass

    @staticmethod
    def get_project(repo_name):
        try:
            project = PM_Project.objects.get(repository=repo_name)
        except PM_Project.DoesNotExist:
            project = None
        return project

    @staticmethod
    def get_user(username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        return user