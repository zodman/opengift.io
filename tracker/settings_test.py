# Django settings for tracker project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Egor', 'gvamm3r@gmail.com'),
)

MANAGERS = ADMINS



# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Moscow'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru-ru'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'
WIKI_IMAGES_PATH = 'PManager/static/upload/wiki%aid/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "/projects/heliard/PManager/static",
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '%n#5@8#8qxv@&amp;d7r^w#e_ygja@8*=pq^5q6k)%l&amp;yy@f-%p8ey'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'tracker.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'tracker.wsgi.application'

import os.path
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__),'templates').replace('\\','/'),
    os.path.join(os.path.dirname(__file__),'../PManager/widgets').replace('\\','/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    'rest_framework',
    # 'robokassa',
    'PManager',
    'pymorphy',
    'django.contrib.humanize',
    'south',
    'django_notify',
    'mptt',
    'sekizai',
    'sorl.thumbnail',
    'wiki',
    'wiki.plugins.attachments',
    'wiki.plugins.notifications',
    'wiki.plugins.images',
    'wiki.plugins.macros',
    'gunicorn',
    'less',
    # 'haystack'
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "PManager.context_processors.get_current_path",
    "PManager.context_processors.get_head_variables",

    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "sekizai.context_processors.sekizai",
)
PYMORPHY_DICTS = {
    'ru': { 'dir': os.path.join(os.path.dirname(__file__), '../PManager/dicts/ru.sqlite-json') },
    }

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

SESSION_COOKIE_HTTPONLY = False
SESSION_COOKIE_SECURE = False
SET_COOKIE = {}

AUTH_PROFILE_MODULE = 'PManager.PM_User'

ORDERS_REDIS_HOST = 'localhost'
ORDERS_REDIS_PORT = 6379
ORDERS_REDIS_PASSWORD = None
ORDERS_REDIS_DB = None

ALLOWED_HOSTS = [
    'heliard',
    'heliard.ru',
    'heliard.dev',
    'localhost'
]

# HAYSTACK_CONNECTIONS = {
#     'default': {
#         'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
#     },
# }


ROBOKASSA_LOGIN = 'HeliardErp'
ROBOKASSA_PASSWORD1 = 'EDEcsE3H7aqpzSpPfsWZ'
ROBOKASSA_PASSWORD2 = '6DVTJQmDNuEzDSEh0stf'
# ROBOKASSA_TEST_MODE = True
ROBOKASSA_EXTRA_PARAMS = ['user']

COMISSION = 1
USE_GIT_MODULE = False

DEBUG = True
# from databases.database import DATABASES
SOUTH_TESTS_MIGRATE = False
DATABASES = dict()
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3'
}
SESSION_COOKIE_DOMAIN = 'heliard.dev'
SOCKET_SERVER_ADDRESS = 'localhost'
project_root = '/projects/heliard/'

# GIT MODULE SETTINGS
USE_GIT_MODULE = False
GITOLITE_ACCESS_URL = 'heliard@localhost'
GITOLITE_ADMIN_REPOSITORY = '/projects/heliard/gitolite-admin'
GITOLITE_REPOS_PATH = '/projects/heliard/repositories'