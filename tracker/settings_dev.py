# -*- coding:utf-8 -*-
__author__ = 'Tonakai'
DEBUG = True
# from databases.database import DATABASES
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'tracker',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': '771VYCH7hj1vp8K',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
    }
}

SESSION_COOKIE_DOMAIN = '46.101.145.165'
SOCKET_SERVER_ADDRESS = 'localhost'
project_root = '/root/heliard/'

# GIT MODULE SETTINGS
USE_GIT_MODULE = False
GITOLITE_ACCESS_URL = 'root@localhost'
GITOLITE_ADMIN_REPOSITORY = '/root/heliard/gitolite-admin'
GITOLITE_REPOS_PATH = '/root/heliard/repositories'
