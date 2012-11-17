import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{ project_name }}.settings')

from django.core.wsgi import get_wsgi_application
from raven.contrib.django.middleware.wsgi import Sentry
application = Sentry(get_wsgi_application())
