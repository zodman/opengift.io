__author__ = 'Gvammer'
DEBUG = False
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
GITOLITE_ADMIN_REPOSITORY = '/home/heliard/gitolite-admin'
