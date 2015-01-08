# -*- coding:utf-8 -*-
__author__ = 'Gvammer'

from databases.database import DATABASES

# DEBUG = True
# TEMPLATE_DEBUG = DEBUG

SESSION_COOKIE_DOMAIN = '127.0.0.1'
SOCKET_SERVER_ADDRESS = '127.0.0.1'
project_root = 'D:/Home/tracker/'
# GIT MODULE SETTINGS
USE_GIT_MODULE = True
GITOLITE_ADMIN_REPOSITORY = 'D:/Home/heliard/gitolite-admin'
GITOLITE_ACCESS_URL = 'heliard@heliard.dev'
GITOLITE_REPOS_PATH = 'D:/Home/heliard/repositories'

CACHES = {
    'default': {
       'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    'git_diff_cache': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/vagrant/PManager/static/cache',
    }
}