"""
Local Django Settings File

INSTRUCTIONS
SAVE A COPY OF THIS FILE IN THIS DIRECTORY WITH THE NAME local_settings.py
MAKE YOUR LOCAL SETTINGS CHANGES IN THAT FILE AND DO NOT CHECK IT IN
CHANGES TO THIS FILE SHOULD BE TO ADD/REMOVE SETTINGS THAT NEED TO BE
MADE LOCALLY BY ALL INSTALLATIONS

local_settings.py, once created, should never be checked into source control
It is ignored by default by .gitignore, so if you don't mess with that, you should be fine.
"""
# pylint: disable=R0801, W0611
import os
import socket

# Set the root path of the project so it's not hard coded
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# Explicitly Define test runner to silence 1_6.W001 Warning
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

DEBUG = eval(os.environ.get("DEBUG", "True"))
TEMPLATE_DEBUG = DEBUG

# Domain Name to Prepend to MEDIA URL, used in feeds
MEDIA_DOMAIN = ""

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
if MEDIA_DOMAIN != "":
    MEDIA_URL = "http://{0}/media/".format(MEDIA_DOMAIN)  # this maps inside of a static_urls URL in gondor.yml
else:
    MEDIA_URL = "/media/"  # make sure this maps inside of a static_urls URL in gondor.yml

# Absolute path to the directory that holds media.
# Note that as of Django 1.3 - media is for uploaded files only.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'mediaroot')

# Staticfiles Config
STATIC_ROOT = PROJECT_ROOT + "/staticroot/"
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(PROJECT_ROOT, "themes", "pb2-jq", "static"), ]
TEMPLATE_DIRS = [os.path.join(PROJECT_ROOT, "themes", "pb2-jq", 'templates'), ]

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# List of callables that add their data to each template
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'podiobooks.core.context_processors.js_api_keys',
    'podiobooks.core.context_processors.current_site',
    'podiobooks.core.context_processors.feed_settings',
    'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
    'podiobooks.core.middleware.StripAnalyticsCookies',
    'django.middleware.gzip.GZipMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'x_robots_tag_middleware.middleware.XRobotsTagMiddleware',
    #    'podiobooks.feeds.middleware.ga_tracking.GATracker',
    'podiobooks.feeds.middleware.redirect_exception.RedirectException',
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'podiobooks.core.middleware.PermanentRedirectMiddleware',
)

ROOT_URLCONF = 'podiobooks.urls'

INSTALLED_APPS = (
    'adminactions',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django_jenkins',
    'mub',
    'noodles',
    'podiobooks',
    'podiobooks.ads',
    'podiobooks.core',
    'podiobooks.libsyn',
    'podiobooks.feeds',
    'podiobooks.search',
    'podiobooks.ratings',
)

# ## DATABASE SETTINGS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'pb2.db'),
        'USER': 'pb2',
        'PASSWORD': '',
    }
}
FIXTURE_DIRS = {os.path.join(PROJECT_ROOT, "..", "..", "podiobooks_data")}

# ## CACHE SETTINGS
CACHE_MIDDLEWARE_SECONDS = int(os.environ.get("CACHE_MIDDLEWARE_SECONDS", "5200"))
CACHE_MIDDLEWARE_ALIAS = os.environ.get("CACHE_MIDDLEWARE_ALIAS", "default")
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
    },
    'locmem': {
         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
    },
    'redis': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}

# Celery Setup
BROKER_URL = 'memory'
CELERY_ALWAYS_EAGER = True  # Force immediate running of async tasks on dev

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Denver'

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ.get("SECRET_KEY", 'zv$+w7juz@(g!^53o0ai1u082)=jkz9my_r=3)fglrj5t8l$2#')

# # Allowed domains to connect
ALLOWED_HOSTS = ['.podiobooks.com', '.cyface.com']

# Permissions for File Uploads
FILE_UPLOAD_PERMISSIONS = 0640

# ## Email
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = os.environ.get("EMAIL_PORT", 587)
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = True
MANAGERS = (('Podiobooks DEV', 'podiobooksdev@gmail.com'),)
ADMINS = (('Podiobooks DEV', 'podiobooksdev@gmail.com'),)
SEND_BROKEN_LINK_EMAILS = eval(os.environ.get("SEND_BROKEN_LINK_EMAILS", "False"))

# #### Custom Variables Below Here #######

# Set a default timeout for external URL grabs, such as for the comments and for Google Analytics from Feeds
socket.setdefaulttimeout(2)  # 2 second timeout for grabbing feed

# # Cover Localization
LOCALIZED_COVER_PLACEHOLDER = STATIC_URL + "images/cover-placeholder.jpg"
USE_COVER_PLACEHOLDERS_ONLY = False

# # Nginx Accel Redirect for favicon and robots
ACCEL_REDIRECT = eval(os.environ.get("ACCEL_REDIRECT", "False"))

# Google Analytics ID
GOOGLE_ANALYTICS_ID = os.environ.get("GOOGLE_ANALYTICS_ID", "UA-5071400-1")

# Facebook Application ID
FACEBOOK_APP_ID = os.environ.get("FACEBOOK_APP_ID", "155134080235")

# <meta name="descripton"> default value
BASE_META_DESCRIPTION = "Free audio books delivered as podcasts. Subscribe for free to any book and start from chapter one. Podiobooks.com"

# ## TIPJAR
TIPJAR_BUSINESS_NAME = 'evo@podiobooks.com'

# ## MUB
MUB_CSS_ORDER = (
    ("jquery.pbshelf.css", "clear.css", "styles.css", "base-shelf.css"),
    ("ads.css", "gsc-overrides.css", "adaptive.css", "small-screen.css")
)
MUB_MINIFY = eval(os.environ.get("MUB_MINIFY", "False"))

# This is to catch special domain names and redirect them to the main
REDIRECT_DOMAINS = os.environ.get("REDIRECT_DOMAINS",[])

# Google Robots Tag Config, in prod you must change this or the site won't be indexed
X_ROBOTS_TAG = os.environ.get("X_ROBOTS_TAG", ['noindex', 'nofollow'])

# URL to Use for Feeds
FEED_DOMAIN = os.environ.get("FEED_DOMAIN", "")
if FEED_DOMAIN != "":
    FEED_URL = "http://{0}".format(FEED_DOMAIN)
else:
    FEED_URL = ""

# ## Debug Toolbar
# http://django-debug-toolbar.readthedocs.org/en/1.4/installation.html#explicit-setup
DEBUG_TOOLBAR_PATCH_SETTINGS = False
INTERNAL_IPS = "127.0.0.1"
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False
}

# ## LOGGING
LOGGING = {
    'version': 1,
    "disable_existing_loggers": False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        "root": {
            "handlers": ["console"],
            'propagate': True,
            "level": "INFO",
        },
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}


# ## LOCAL SETTINGS OVERRIDES
try:
    from podiobooks.settings_local import *
except ImportError:
    pass
