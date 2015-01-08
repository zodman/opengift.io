# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
DEBUG = True
TEMPLATE_DEBUG = DEBUG
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
SESSION_COOKIE_DOMAIN = 'heliard.ru'
SOCKET_SERVER_ADDRESS = 'heliard.ru'
project_root = '/home/heliard/heliard/'
# GIT MODULE SETTINGS
USE_GIT_MODULE = True
GITOLITE_ADMIN_REPOSITORY = '/home/heliard/gitolite-admin'
GITOLITE_ACCESS_URL = 'heliard@heliard.ru'
GITOLITE_REPOS_PATH = '/home/heliard/repositories'

CACHES = {
    'default': {
       'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    'git_diff_cache': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/home/heliard/heliard/PManager/static/cache',
    }
}
