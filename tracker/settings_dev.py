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
project_root = '/home/heliard/heliard/'

# GIT MODULE SETTINGS
USE_GIT_MODULE = False
GITOLITE_ACCESS_URL = 'heliard@localhost'
GITOLITE_ADMIN_REPOSITORY = '/home/heliard/gitolite-admin'
GITOLITE_REPOS_PATH = '/home/heliard/repositories'
GITOLITE_DEFAULT_USER = 'id_rsa'
