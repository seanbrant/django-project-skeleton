import os

from dj_database_url import config as database_config
from memcacheify import memcacheify


PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

DEBUG = os.environ.get('DEBUG', 'false') == 'true'
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = os.environ.get('SECRET_KEY', None)

ROOT_URLCONF = '{{ project_name }}.urls'
WSGI_APPLICATION = '{{ project_name }}.wsgi.application'
SITE_ID = 1

INTERNAL_IPS = ['127.0.0.1']

ADMINS = [
    # ('Your Name', 'your_email@example.com'),
]
MANAGERS = ADMINS

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'public', 'uploads')
MEDIA_URL = '/uploads/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'public', 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(PROJECT_ROOT, 'static')]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

DEFAULT_FILE_STORAGE = os.environ.get('DEFAULT_FILE_STORAGE', 'django.core.files.storage.FileSystemStorage')

TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]
if os.environ.get('USE_CACHE_TEMPLATE_LOADER', 'false') == 'true':
    TEMPLATE_LOADERS = [
        ('django.template.loaders.cached.Loader', TEMPLATE_LOADERS),
    ]

TEMPLATE_DIRS = [os.path.join(PROJECT_ROOT, 'templates')]

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'raven.contrib.django.middleware.SentryResponseErrorIdMiddleware',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'debug_toolbar',
    'django_jenkins',
    'gunicorn',
    'pipeline',
    'raven.contrib.django',
    'south',

    # '{{ project_name }}.app1',
    # '{{ project_name }}.app2',
]

DATABASES = database_config(default='sqlite:///{}'.format(os.path.join(PROJECT_ROOT, '{{ project_name }}.db')))
if 'postgresql' in DATABASES['default']['ENGINE']:
    DATABASES['default']['ENGINE'] = 'django_postgrespool'
    SOUTH_DATABASE_ADAPTERS = {'default': 'south.db.postgresql_psycopg2'}

CACHES = memcacheify()
CACHES['staticfiles'] = dict(CACHES['default'])
CACHES['staticfiles']['TIMEOUT'] = 0  # Never expire

TEST_RUNNER = 'tests.runner.HighlightedDiscoverRunner'
TEST_DISCOVER_ROOT = os.path.join(PROJECT_ROOT, 'tests')

SOUTH_TESTS_MIGRATE = False

JENKINS_TEST_RUNNER = 'tests.runner.CIDiscoverRunner'
JENKINS_TASKS = ['django_jenkins.tasks.django_tests']
PROJECT_APPS = ['{{ project_name }}']

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

PIPELINE_CSS = {
    'master': {
        'source_filenames': ['css/base.css'],
        'output_filename': 'css/master.css',
        'extra_context': {'media': 'screen'}
    }
}

PIPELINE_JS = {
    'master': {
        'source_filenames': [],
        'output_filename': 'js/master.js',
    }
}

PIPELINE_CSS_COMPRESSOR = None
PIPELINE_JS_COMPRESSOR = None

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'sentry': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'raven.contrib.django.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    }
}
