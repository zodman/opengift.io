# -*- coding:utf-8 -*-
__author__ = 'Tonakai'
from django.contrib.auth.models import User
from PManager.models.tasks import PM_Project
from PManager.models.tasks import PM_Timer
from PManager.models.tasks import PM_Task_Message
import logging
from tracker import settings
from git import *
from PManager.classes.git.diff_parser import DiffParser
from django.core.files.storage import FileSystemStorage
if not settings.USE_GIT_MODULE:
    exit("GIT MODULE NOT INSTALLED");
repo = Repo(settings.GITOLITE_ADMIN_REPOSITORY)
logger = logging.getLogger(__name__)


class Warden(object):
    user = None
    project = None
    timer = None

    @property
    def repo_path(self):
        return settings.GITOLITE_REPOS_PATH + '/' + self.project.repository + '.git'

    def __init__(self, username, repository):
        self.user = self.get_user(username)
        self.project = self.get_project(repository)
        if self.user is None or self.project is None:
            raise AssertionError("Cant use empty user or project")

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
        if not self.is_task():
            return 'ERROR: Can\'t find active task'
        _repo = Repo(self.repo_path)
        for _hash in hashes:
            commit_diff = _repo.git.show(_hash)
            df = DiffParser(commit_diff)
            PM_Task_Message.create_commit_message(df, self.user, self.timer.task)

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

    @staticmethod
    def get_diff(message):
        if not message.commit:
            return False
        warden = Warden(message.author, message.project)
        _repo = Repo(warden.repo_path)
        _diff = _repo.git.show(message.commit)
        return DiffParser(_diff)