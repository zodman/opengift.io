# -*- coding:utf-8 -*-
__author__ = 'Tonakai'
DEBUG = True
# from databases.database import DATABASES
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'tracker',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'root',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
    }
}

SESSION_COOKIE_DOMAIN = 'heliard.dev'
SOCKET_SERVER_ADDRESS = 'localhost'
project_root = '/projects/heliard/'

# GIT MODULE SETTINGS
USE_GIT_MODULE = False
GITOLITE_ACCESS_URL = 'heliard@localhost'
GITOLITE_ADMIN_REPOSITORY = '/projects/heliard/gitolite-admin'
GITOLITE_REPOS_PATH = '/projects/heliard/repositories'