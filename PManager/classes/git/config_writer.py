# -*- coding:utf-8 -*-
__author__ = 'Tonakai'
from django.contrib.auth.models import User
from tracker.settings import DOCKER_USER_NAME, GITOLITE_DEFAULT_USER

class ConfigWriter(object):
    @staticmethod
    def write_config(projects):
        output = "repo gitolite-admin\n  RW+     =   " + GITOLITE_DEFAULT_USER + "\n"
        for project in projects:
            output += ConfigWriter.get_include_str(project)
        return output

    @staticmethod
    def get_include_str(project):
        return 'include "' + project + '"\r\n'

    @staticmethod
    def generate_project_str(project):
        project_name = project.repository
        output = ""
        output = output + 'repo ' + project_name + '\n'
        users = User.objects.filter(pk__in=project.projectRoles.values('user_id'))

        user_names = []
        if not users or project.closed:
            output = output + " RW+ = " + GITOLITE_DEFAULT_USER + '\n'
            return output
        for user in users:
            user_names.append(user.username)
        output = output + " RW+ = "
        if DOCKER_USER_NAME is not None or DOCKER_USER_NAME is not False:
            output = output + DOCKER_USER_NAME + " "
        output = output + " ".join(user_names) + '\n'
        return output
