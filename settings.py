# Django settings for orders project.

DEBUG = False 
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('yearbook', 'nwiltsie@mit.edu'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'django.db.backends.sqlite3'
DATABASE_NAME = 'yearbook+scripts'
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

import os.path
if os.path.exists("settings_private.py"):
    execfile("settings_private.py")

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/admin'
FORCE_SCRIPT_NAME = None

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = '/__scripts/django/media/'
ADMIN_MEDIA_PREFIX = '/scripts/static/admin/'

# URL prefix for static files to be served by templates
STATIC_URL = "/scripts/static/"

# Directory where static files live.  ONLY USED IN DEVELOPMENT.
STATICFILES_DIRS = (
    'static',
)

DAJAXICE_MEDIA_PREFIX = 'dajaxice'
DAJAXICE_URL_PREFIX = 'dajaxice'

AUTH_PROFILE_MODULE = 'checkout.User'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.RemoteUserBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '99&xeaxqq+om4i1lhqid#&olgq1crnah#9b)bz(j7kub(s84v9'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    'templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.flatpages',
    'django.contrib.staticfiles',
    'creditcard',
    'seniors',
    'creditcard',
    'mainsite',
    'purchase',
    'dajaxice',
    'dajax',
    'checkout',
    'massadmin'
)

