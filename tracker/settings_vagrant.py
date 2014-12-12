# -*- coding:utf-8 -*-
__author__ = 'Tonakai'
DEBUG = True
# from databases.database import DATABASES
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'tracker',                      # Or path to database file if using sqlite3.
        'USER': 'heliard',                      # Not used with sqlite3.
        'PASSWORD': 'gp7bG7Rcy07jwYS4fAAB',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
    }
}

SESSION_COOKIE_DOMAIN = 'heliard.dev'
SOCKET_SERVER_ADDRESS = 'localhost'
project_root = '/vagrant/'
# GIT MODULE SETTINGS
USE_GIT_MODULE = True
GITOLITE_ADMIN_REPOSITORY = '/home/vagrant/gitolite-admin'
GITOLITE_ACCESS_URL = 'vagrant@heliard.dev'
GIT_PUSH_MESSAGE = u'Автоматически остановлено при коммите в репозиторий'