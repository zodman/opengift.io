from fabric import task
from invoke import run as local

@task
def timing(ctx):
    local(' time DJANGO_SETTINGS_MODULE=tracker.settings PYTHONPATH=. profimp "from PManager.  tests.views import *" --html > tmp/index.html')

@task
def test(ctx):
    cmds = [
        "coverage run --source=.  manage.py test PManager.ViewsTest",
        "coverage report  --skip-covered",
        "coverage html  --skip-covered",
    ]
    for cmd in cmds:
        local(cmd, echo=True)

    #local(' python  -W ignore  manage.py  test  PManager.ViewsTest --traceback --failfast')
