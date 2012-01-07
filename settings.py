# Django settings for Technique project.

import os.path, sys

DEBUG = True 
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Nick Wiltsie', 'nwiltsie@mit.edu'),
    ('Quentin Smith', 'quentin@mit.edu'),
)

DEFAULT_FROM_EMAIL = 'tnq-techno@mit.edu'

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.spatialite',
        'NAME': 'wiki.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': ''             # Set to empty string for default. Not used with sqlite3.
    }
}

# Path to root directory of django project
DJANGO_ROOT = os.path.join( os.path.dirname(os.path.abspath(__file__)) )

#Add wiki to path so apps can be imported without localwiki.sapling prefix
sys.path.append( os.path.join(DJANGO_ROOT, "localwiki") )
sys.path.append( os.path.join(DJANGO_ROOT, "localwiki", "sapling") )

GLOBAL_LICENSE_NOTE = """<p>Except where otherwise noted, this content is licensed under a <a href="http://creativecommons.org/licenses/by/3.0/">Creative Commons Attribution License</a>. See <a href="/Copyrights">Copyrights.</p>"""

EDIT_LICENSE_NOTE = """<p>By clicking "Save Changes" you are agreeing to release your contribution under the <a href="http://creativecommons.org/licenses/by/3.0/" target="_blank">Creative Commons-By license</a>, unless noted otherwise. See <a href="/Copyrights" target="_blank">Copyrights</a>.</p>"""

SIGNUP_TOS = """I agree to release my contributions under the <a href="http://creativecommons.org/licenses/by/3.0/" target="_blank">Creative Commons-By license</a>, unless noted otherwise. See <a href="/Copyrights" target="_blank">Copyrights</a>."""

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/admin/'

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
MEDIA_ROOT = 'media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
#MEDIA_URL = ''
MEDIA_URL = "http://technique.mit.edu/media/"

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = '/__scripts/django/media/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

# URL prefix for static files to be served by templates
STATIC_URL = "/static/"

# Directory where static files live.  ONLY USED IN DEVELOPMENT.
STATICFILES_DIRS = (
    'static',
)

DAJAXICE_MEDIA_PREFIX = 'dajaxice'
DAJAXICE_URL_PREFIX = 'dajaxice'

AUTH_PROFILE_MODULE = 'checkout.User'

AUTHENTICATION_BACKENDS = (
    'users.backends.CaseInsensitiveModelBackend',
    'users.backends.RestrictiveBackend',
    'django.contrib.auth.backends.RemoteUserBackend',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
    }
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = '99&xeaxqq+om4i1lhqid#&olgq1crnah#9b)bz(j7kub(s84v9'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'util.middleware.RequireLoginMiddleware',
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
    'django.contrib.staticfiles',
    'creditcard',
    'seniors',
    'mainsite',
    'purchase',
    'dajaxice',
    'dajax',
    'checkout',
    'massadmin',
    'lg',
)

######################################################################
###  Localwiki Stuff
######################################################################

#Generally views should be protected with the @login_required decorator;
#this is a convenience that works with the util.middleware.LoginRequiredMiddleware
#because we want to protect ALL wiki views.
LOGIN_REQUIRED_URLS = (
    '/wiki/',
)

PROJECT_ROOT = 'localwiki/sapling'

# users app settings
USERS_ANONYMOUS_GROUP = 'Anonymous'
USERS_BANNED_GROUP = 'Banned'
USERS_DEFAULT_GROUP = 'Authenticated'
USERS_DEFAULT_PERMISSIONS = {'auth.group':
                                [{'name': USERS_DEFAULT_GROUP,
                                  'permissions':
                                    [['add_mapdata', 'maps', 'mapdata'],
                                     ['change_mapdata', 'maps', 'mapdata'],
                                     ['delete_mapdata', 'maps', 'mapdata'],
                                     ['add_page', 'pages', 'page'],
                                     ['change_page', 'pages', 'page'],
                                     ['delete_page', 'pages', 'page'],
                                     ['add_pagefile', 'pages', 'pagefile'],
                                     ['change_pagefile', 'pages', 'pagefile'],
                                     ['delete_pagefile', 'pages', 'pagefile'],
                                     ['add_redirect', 'redirects', 'redirect'],
                                     ['change_redirect', 'redirects', 'redirect'],
                                     ['delete_redirect', 'redirects', 'redirect'],
                                    ]
                                 },
                                 {'name': USERS_ANONYMOUS_GROUP,
                                  'permissions':
                                    [['add_mapdata', 'maps', 'mapdata'],
                                     ['change_mapdata', 'maps', 'mapdata'],
                                     ['delete_mapdata', 'maps', 'mapdata'],
                                     ['add_page', 'pages', 'page'],
                                     ['change_page', 'pages', 'page'],
                                     ['delete_page', 'pages', 'page'],
                                     ['add_pagefile', 'pages', 'pagefile'],
                                     ['change_pagefile', 'pages', 'pagefile'],
                                     ['delete_pagefile', 'pages', 'pagefile'],
                                     ['add_redirect', 'redirects', 'redirect'],
                                     ['change_redirect', 'redirects', 'redirect'],
                                     ['delete_redirect', 'redirects', 'redirect'],
                                    ]
                                 },
                                ]
                            }

# django-guardian setting
ANONYMOUS_USER_ID = -1

# By default we load only one map layer on most pages to speed up load
# times.
OLWIDGET_INFOMAP_MAX_LAYERS = 1

# Should we display user's IP addresses to non-admin users?
SHOW_IP_ADDRESSES = False

LOGIN_REDIRECT_URL = '/'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE':'',
        'URL' : ''
    },
}

HAYSTACK_SITECONF = 'sapling.search_sites'
HAYSTACK_SEARCH_ENGINE = 'dummy'

THUMBNAIL_BACKEND = 'utils.sorl_backends.AutoFormatBackend'

OL_API = STATIC_URL + 'openlayers/OpenLayers.js?tm=1317359250'
OLWIDGET_CSS = '%solwidget/css/sapling.css?tm=1317359250' % STATIC_URL
OLWIDGET_JS = '%solwidget/js/olwidget.js?tm=1317359250' % STATIC_URL
CLOUDMADE_API = '%solwidget/js/sapling_cloudmade.js?tm=1317359250' % STATIC_URL

TEMPLATE_CONTEXT_PROCESSORS = (
    "utils.context_processors.sites.current_site",
    "utils.context_processors.settings.license_agreements",
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.csrf",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "staticfiles.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    "staticfiles.context_processors.static",
)

MIDDLEWARE_CLASSES += (
    'django.contrib.messages.middleware.MessageMiddleware',
    'versionutils.versioning.middleware.AutoTrackUserInfoMiddleware',
    'redirects.middleware.RedirectFallbackMiddleware',
)

INSTALLED_APPS += (
    'django.contrib.gis',
    'django.contrib.messages',
    'django.contrib.sites',

    # Other third-party apps
    'haystack',
    'olwidget',
    'registration',
    'sorl.thumbnail',
    'guardian',
    'south',
    'staticfiles',

    # Our apps
    'versionutils.versioning',
    'versionutils.diff',
    'ckeditor',
    'pages',
    'maps',
    'users',
    'recentchanges',
    'search',
    'redirects',
    'utils',
)

SITE_THEME = 'sapling'

OLWIDGET_DEFAULT_OPTIONS = {
    'default_lat': 42.359083,
    'default_lon': -71.094761,
    'default_zoom': 16,
    'zoom_to_data_extent_min': 16,

    'layers': ['cloudmade.35165', 've.aerial'],
    'map_options': {
        'controls': ['Navigation', 'PanZoomBar', 'KeyboardDefaults'],
        'theme': '/static/openlayers/theme/sapling/style.css',
    },
    'overlay_style': {'fillColor': '#ffc868',
                      'strokeColor': '#db9e33',
                      'strokeDashstyle': 'solid'},
    'map_div_class': 'mapwidget',
}

###############################
# Setup template directories
###############################
PROJECT_TEMPLATE_DIR = os.path.join(PROJECT_ROOT, 'templates')

PROJECT_THEME_TEMPLATE_DIR = os.path.join(PROJECT_ROOT, 'themes', SITE_THEME, 'templates')

TEMPLATE_DIRS += (
    PROJECT_TEMPLATE_DIR,
    PROJECT_THEME_TEMPLATE_DIR,
)

STATICFILES_FINDERS = (
    "staticfiles.finders.FileSystemFinder",
    "staticfiles.finders.AppDirectoriesFinder"
)

_global_theme_dir = os.path.join(PROJECT_ROOT, 'themes', SITE_THEME, 'assets')

if os.path.exists(_global_theme_dir):
    STATICFILES_DIRS += (('theme', _global_theme_dir),)

STATIC_ROOT = os.path.join(DJANGO_ROOT, "staticfiles")

if os.path.exists("settings_private.py"):
    execfile("settings_private.py")
