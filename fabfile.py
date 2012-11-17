import os

from fabric.api import env, local, require


def production():
    env.app = os.environ.get('PRODUCTION_APP_NAME')
    env.branch = os.environ.get('PRODUCTION_BRANCH', '')
    env.newrelic = {
        'API_KEY': os.environ.get('PRODUCTION_NEWRELIC_API_KEY', None),
        'ACCOUNT_ID': os.environ.get('PRODUCTION_NEWRELIC_ACCOUNT_ID', None),
        'APP_ID': os.environ.get('PRODUCTION_NEWRELIC_APP_ID', None),
    }


def staging():
    env.app = os.environ.get('STAGING_APP_NAME')
    env.branch = os.environ.get('STAGING_BRANCH', 'development')
    env.newrelic = {
        'API_KEY': os.environ.get('STAGING_NEWRELIC_API_KEY', None),
        'ACCOUNT_ID': os.environ.get('STAGING_NEWRELIC_ACCOUNT_ID', None),
        'APP_ID': os.environ.get('STAGING_NEWRELIC_APP_ID', None),
    }


def run_ci_tests():
    local('virtualenv venv')
    local('venv/bin/pip install -r requirements.txt')
    local('mkdir -p reports')
    local('venv/bin/coverage run --source={{ project_name }} --branch manage.py jenkins --settings=tests.settings')
    local('venv/bin/coverage xml --omit="*migrations*" -o reports/coverage.xml')
    local('venv/bin/coverage html --omit="*migrations*" -d reports/coverage')
    local('venv/bin/coverage erase')
    local('venv/bin/pep8 --ignore=E128,E501,E124 --exclude="*migrations*" {{ project_name }} > reports/pep8.report; exit 0;')
    local('venv/bin/pyflakes `find {{ project_name }} -name "*.py" -not -iwholename "*/migrations/*" | xargs` > reports/pyflakes.report; exit 0;')


def make_docs():
    local('rm -rf docs/_build')
    local('sphinx-build -b html -d docs/_build/doctrees docs docs/_build/html')


def ping(direction='enabled'):
    require('app', provided_by=['production', 'staging'])
    require('newrelic', provided_by=['production', 'staging'])
    if all(env.newrelic.values()):
        local('curl https://heroku.newrelic.com/accounts/{ACCOUNT_ID}/'
              'applications/{APP_ID}/ping_targets/{DIRECTION} '
              '-X POST -H "X-Api-Key: {API_KEY}"'.format(DIRECTION=direction, **env.newrelic))


def maintenance(direction='on'):
    require('app', provided_by=['production', 'staging'])
    ping(direction == 'on' and 'disable' or 'enable')
    local('heroku maintenance:{} --app {}'.format(direction, env.app))


def syncdb():
    require('app', provided_by=['production', 'staging'])
    local('heroku run python manage.py migrate --noinput --app {}'.format(env.app))


def collectstatic():
    require('app', provided_by=['production', 'staging'])
    local('heroku run python manage.py collectstatic --noinput --app {}'.format(env.app))


def deploy():
    require('app', provided_by=['production', 'staging'])
    require('branch', provided_by=['production', 'staging'])
    maintenance('on')
    commit = ':'.join(bit for bit in [os.environ.get('GIT_COMMIT', env.branch), 'master'] if bit)
    local('git push -f git@heroku.com:{}.git {}'.format(env.app, commit))
    syncdb()
    collectstatic()
    maintenance('off')
