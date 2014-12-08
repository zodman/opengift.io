# -*- coding:utf-8 -*-
import base64
import struct

__author__ = 'Tonakai'
import os
import os.path
import re
import glob
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from PManager.classes.git.config_writer import ConfigWriter
from git import *
from tracker import settings
# bug due to wrong os.getlogin argument
# http://stackoverflow.com/questions/4399617/python-os-getlogin-problem
import pwd
os.getlogin = lambda: pwd.getpwuid(os.getuid())[0]

__all__ = ['os', 'FileSystemStorage', 'ContentFile', 'ConfigWriter']


class GitoliteManager(object):
    KEYDIR = ''
    CONF_DIR = ''
    CONF_FILE = ''
    fs = {}
    repo = {}

    # key management
    @classmethod
    def get_index(cls):
        return cls.repo.index

    @classmethod
    def install_params(cls):
        cls.KEYDIR = 'keydir'
        cls.CONF_DIR = 'conf'
        cls.CONF_FILE = cls.CONF_DIR + '/gitolite.conf'
        cls.fs = FileSystemStorage(location=settings.GITOLITE_ADMIN_REPOSITORY)
        cls.repo = Repo(settings.GITOLITE_ADMIN_REPOSITORY)

    @classmethod
    def commit(cls, _index, message):
        _index.commit(message)
        cls.repo.remotes.origin.push()
        return True

    @classmethod
    def check_key(cls, data):
        try:
            tp, key_string, comment = data.split()
            key_data = base64.decodestring(key_string)
            int_len = 4
            str_len = struct.unpack('>I', key_data[:int_len])[0]
            result = key_data[int_len:int_len+str_len] == tp
        except ValueError:
            return False
        else:
            return result

    @classmethod
    def add_key_to_user(cls, user, name, data):
        file_path = cls.get_key_file(name, user)
        if cls.is_key_exists(file_path):
            return ""
        file_path = cls.fs.save(file_path, ContentFile(data))
        index = cls.get_index()
        index.add([file_path, ])
        message = "Added key %s for %s" % (name, user.username)
        cls.commit(index, message)
        if cls.is_success(message):
            return file_path
        return ""

    @classmethod
    def is_success(cls, message):
        _log = cls.repo.head.reference.log()
        return re.search(message, str(_log[-1]))

    @classmethod
    def remove_key_from_user(cls, key, user):
        if not cls.is_key_exists(key.file_path):
            return True
        cls.fs.delete(key.file_path)
        index = cls.get_index()
        index.remove([key.file_path, ])
        message = "Removed key %s for %s" % (key.name, user.username)
        res = cls.commit(index, message)
        if cls.is_success(message):
            return res
        return False

    @classmethod
    def get_suggested_name(cls, reponame):
        proj_path = cls.fs.get_available_name(cls.get_project_conf_name(reponame))
        m = re.match(cls.CONF_DIR + "/(?P<repository>\w+).conf", proj_path)
        if not m:
            return False
        matches = m.groupdict()
        if matches['repository']:
            return matches['repository']
        return False

    @classmethod
    def get_key_file(cls, name, user):
        return "%s/%s@%s.pub" % (cls.KEYDIR, user.username, name)

    @staticmethod
    def is_key_exists(keyfile):
        return os.path.isfile(settings.GITOLITE_ADMIN_REPOSITORY + "/" + keyfile)

    @classmethod
    def repository_exists(cls, rep_name):
        path = settings.GITOLITE_ADMIN_REPOSITORY + '/' + GitoliteManager.get_project_conf_name(rep_name)
        return os.path.isfile(path)

    @classmethod
    def add_repo(cls, project, user):
        rep_name = project.repository
        if not rep_name:
            return False
        username = user.username
        project_config = cls.get_project_conf_name(rep_name)
        if(cls.fs.exists(project_config)):
            cls.fs.delete(project_config)
        permissions = cls.generate_project_permissions(project)
        cls.update_main_config()
        index = cls.get_index()
        index.add([project_config, cls.CONF_FILE, ])
        message = "Added repo %s for %s" % (rep_name, username)
        res = cls.commit(index, message)
        if cls.is_success(message):
            return res
        return False

    @classmethod
    def get_project_conf_name(cls, rep_name):
        return "%s/%s.conf" % (cls.CONF_DIR, rep_name)

    @classmethod
    def remove_repo(cls, project):
        rep_name = project.repository
        project_config = cls.get_project_conf_name(rep_name)
        cls.fs.delete(project_config)
        cls.update_main_config()
        index = cls.get_index()
        index.remove([project_config, ])
        index.add([cls.CONF_FILE, ])
        message = "Removed repo %s for %s" % (rep_name, project.author)
        res = cls.commit(index, message)
        if cls.is_success(message):
            return res
        return False

    @classmethod
    def update_main_config(cls):
        projects = glob.glob(settings.GITOLITE_ADMIN_REPOSITORY + "/" + cls.CONF_DIR + '/*.conf')
        if not projects:
            return False
        projects.remove(settings.GITOLITE_ADMIN_REPOSITORY + '/' +  cls.CONF_FILE)
        data = ConfigWriter.write_config(projects)
        if(cls.fs.exists(cls.CONF_FILE)):
            cls.fs.delete(cls.CONF_FILE)
        cls.fs.save(cls.CONF_FILE, ContentFile(data))
        return True

    @classmethod
    def generate_project_permissions(cls, project):
        data = ConfigWriter.generate_project_str(project)
        cls.fs.save(cls.CONF_DIR + "/" + project.repository + ".conf", ContentFile(data))
        return True

    @classmethod
    def regenerate_access(cls, project):
        rep_name = project.repository
        project_config = cls.get_project_conf_name(rep_name)
        if(cls.fs.exists(project_config)):
            cls.fs.delete(project_config)
        permissions = cls.generate_project_permissions(project)
        index = cls.get_index()
        index.add([project_config,])
        message = "Regenerated access for repo %s" % (rep_name)
        res = cls.commit(index, message)
        if cls.is_success(message):
            return res
        return False

if settings.USE_GIT_MODULE:
    GitoliteManager.install_params()