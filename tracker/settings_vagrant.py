# -*- coding:utf-8 -*-
__author__ = 'Tonakai'
DEBUG = True
# from databases.database import DATABASES
DATABASES = {
    'default_old': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'tracker',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'root',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
    },
    'replica': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'tracker_test',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'root',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
        'TEST_MIRROR': 'default'
    },
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'tracker_10_03_2015',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'root',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306'
    }
}

SESSION_COOKIE_DOMAIN = 'heliard.dev'
SOCKET_SERVER_ADDRESS = 'localhost'
project_root = '/vagrant/'
# GIT MODULE SETTINGS
USE_GIT_MODULE = True
GITOLITE_ADMIN_REPOSITORY = '/home/vagrant/gitolite-admin'
GITOLITE_ACCESS_URL = 'vagrant@heliard.dev'
GITOLITE_REPOS_PATH = '/home/vagrant/repositories'

# TODO: change to dummycache when caching is tested
#'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
CACHES = {
    'default': {
       'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    'git_diff_cache': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/vagrant/PManager/static/cache',
    }
}
