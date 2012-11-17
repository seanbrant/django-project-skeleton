web: newrelic-admin run-program gunicorn {{ project_name }}.wsgi -w 4 -b 0.0.0.0:$PORT -k gevent --max-requests 250
# worker: newrelic-admin run-program python manage.py celeryd -E -B --loglevel=INFO
