# -*- coding:utf-8 -*-
__author__ = 'Tonakai'
from django.contrib.auth.models import User
from PManager.models.tasks import PM_Project
from PManager.models.tasks import PM_Timer
from PManager.models.tasks import PM_Task_Message
from PManager.classes.server.message import RedisMessage
from PManager.viewsExt.tools import emailMessage
from PManager.viewsExt.tools import service_queue
import logging
import datetime
from django.utils import timezone
from tracker import settings
from git import *

from PManager.classes.git.diff_parser import DiffParser
from PManager.classes.sniffer.js_sniffer import JSSniffer
from PManager.classes.sniffer.php_sniffer import PHPSniffer
from django.core.files.storage import FileSystemStorage


if not settings.USE_GIT_MODULE:
    exit("GIT MODULE NOT INSTALLED")
repo = Repo(settings.GITOLITE_ADMIN_REPOSITORY)
logger = logging.getLogger(__name__)
import os


class Warden(object):
    user = None
    project = None
    timer = None

    @property
    def repo_path(self):
        return settings.GITOLITE_REPOS_PATH + '/' + self.project.repository + '.git'

    def __init__(self, username, repository, is_loaded=False):
        if not is_loaded:
            self.user = self.get_user(username)
            self.project = self.get_project(repository)
        else:
            self.user = username
            self.project = repository
        if self.user is None or self.project is None:
            raise AssertionError("Can't use empty user or project")

    def is_task(self):
        try:
            timer = PM_Timer.objects.get(user=self.user, dateEnd__isnull=True, project=self.project)
            logger.info(u'Active timer found. User: {0:s} Project: {1:s}'.format(self.user, self.project))
        except PM_Timer.DoesNotExist:
            timer = PM_Timer.objects.get(user=self.user, project=True).order_by('-dateEnd')
            timer = timer[0] if timer else None

        if timer and timer.task.project == self.project:
            self.timer = timer
            return 'true'
        else:
            logger.info(u'Active timer not found. User: {0:s} Project: {1:s}'.format(self.user, self.project))
        return 'false'

    def write_message(self, ref, hashes):
        if not self.is_task():
            return 'ERROR: Can\'t find active task'
        _repo = Repo(self.repo_path)
        for _hash in hashes:
            commit_diff = _repo.git.show(_hash)
            try:
                df = DiffParser(commit_diff)
                comment = PM_Task_Message.create_commit_message(df, self.user, self.timer.task)
                mess = RedisMessage(
                    service_queue,
                    objectName='comment',
                    type='add',
                    fields=comment.getJson({'noveltyMark': True})
                )
                mess.send()

                ar_email = comment.task.getUsersEmail([self.user.id])
                task_data = {
                    'task_url': comment.task.url,
                    'name': comment.task.name,
                    'dateCreate': timezone.make_aware(datetime.datetime.now(), timezone.get_current_timezone()),
                    'comment': {
                        'text': comment.text,
                        'author': ' '.join([comment.author.first_name, comment.author.last_name])
                    }
                }
                mail_sender = emailMessage(
                    'new_task_commit',
                    {
                        'task': task_data
                    },
                    u'Коммит: ' + task_data['name']
                )

                try:
                    mail_sender.send(ar_email)
                except Exception:
                    print 'Email has not sent'

            except IOError:
                return 'ERROR: Commit #' + commit_diff + ' could not be parsed'

    @staticmethod
    def get_project(repo_name):
        try:
            project = PM_Project.objects.get(repository=repo_name, locked=False, closed=False)
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
        try:
            warden = Warden(message.author, message.project, is_loaded=True)
        except AssertionError:
            return False
        _repo = Repo(warden.repo_path)
        try:
            _diff = _repo.git.show(message.commit, U=10)
            df = DiffParser(_diff)
            df = Warden.sniff_files(_repo, df, message)
        except IOError:
            return False

        return df

    @staticmethod
    def sniff_files(_repo, df, message):
        for d in df.files:
            ext = d.path.split('.').pop()
            if ext == 'php' or ext == 'js':
                r = _repo.git.show(message.commit + ':' + d.path[1:])
                if r:
                    filename = 'tracker/sniffer_files/tmp' + str(message.author.id)
                    f = open(filename, 'w')
                    f.write(r)
                    f.close()

                    sniffer_report = []
                    if ext == 'php':
                        sniffer_report = PHPSniffer.sniff(filename)
                    elif ext == 'js':
                        sniffer_report = JSSniffer.sniff(filename)
                    d.error_qty = len(sniffer_report)
                    os.remove(filename)
        return df
