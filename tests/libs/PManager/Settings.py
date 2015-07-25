# -*- coding:utf-8 -*-
__author__ = 'Rayleigh'
__version__ = '0.0.1'
ROBOT_LIBRARY_SCOPE = 'GLOBAL'
ROBOT_LIBRARY_VERSION = '0.0.1'

from tracker import settings


class Settings:

    def __init__(self):
        pass

    @staticmethod
    def get_settings(name):
        return getattr(settings, name, None)

    @staticmethod
    def get_project_root():
        return settings.PROJECT_ROOT

    @staticmethod
    def get_root_url():
        return settings.HTTP_ROOT_URL

    @staticmethod
    def get_maildumper_url():
        return str(settings.EMAIL_HOST) + ':1080'
