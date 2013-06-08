from datetime import datetime
from operator import add
from os.path import join
from random import sample
from time import sleep

from fabric.api import abort, cd, env, execute, hide, prefix, prompt, require
from fabric.colors import green, red, yellow
from fabric.contrib import files
import fabric.api


def run(command, shell=True, pty=True, combine_stderr=True):
    "Run with virtualenvwrapper functions loaded"
    with prefix('source /etc/bash_completion.d/virtualenvwrapper'):
        return fabric.api.run(command, shell, pty, combine_stderr)


def verun(command, shell=True, pty=True, combine_stderr=True):
    "Run inside virtual_env"
    require('name')
    with prefix('source /etc/bash_completion.d/virtualenvwrapper'),\
            prefix('workon {name}'.format(**env)):
        return fabric.api.run(command, shell, pty, combine_stderr)


def pyrun(command, shell=True, pty=True, combine_stderr=True):
    "Run inside virtual_env, passing the command to `python -c`"
    command = command.replace('"', '\\\\"')
    return verun('python -c "{}"'.format(command))


def manage(command, shell=True, pty=True, combine_stderr=True):
    "Django manage command"
    return verun('manage ' + command, shell, pty, combine_stderr)


def local(command):
    return fabric.api.local(command, capture=True)


def pylocal(command):
    command = command.replace('"', '\\\\"')
    return local('python -c "{}"'.format(command))


def pgrun(cmd):
    with prefix('export PGPASSWORD="{db_password}"'.format(**env)):
        run(cmd)


def target_shared():
    env.user = 'deployer'
    env.home = '/home/{user}'.format(**env)
    env.deploy_to = '{home}/apps/{name}'.format(**env)
    env.shared = '{deploy_to}/shared'.format(**env)
    env.cache = '{shared}/cached-copy'.format(**env)
    env.cache_db = 'etsidata_{target}_cache'.format(**env)
    env.log = '{shared}/log'.format(**env)
    env.static = '{shared}/static'.format(**env)
    env.releases = '{deploy_to}/releases'.format(**env)
    env.release = join(env.releases, datetime.now().strftime('%Y%m%d%H%M%S'))
    env.current = '{deploy_to}/current'.format(**env)
    env.uwsgi_pid = '{shared}/pids/{name}.pid'.format(**env)
    env.uwsgi_socket = '{shared}/sockets/{name}.sock'.format(**env)
    env.uwsgi_ini = '{shared}/config/uwsgi.ini'.format(**env)
    env.uwsgi_log = '{log}/uwsgi.log'.format(**env)

    with hide('everything'):
        execute(get_current_status)


def captcha():
    msg = """\
  !
  !
  !
  !
  ! You're about to affect the PRODUCTION environment!
  !
  ! To confirm your intention, wait a few seconds..."""
    print(yellow(msg))
    sleep(5)

    numbers = sample(xrange(10), 2)
    print(yellow('  ! and answer this arithmetic problem:'))
    answer = prompt(yellow("  ! {} + {} = ".format(*numbers)), validate='\d+')

    if int(answer) == add(*numbers):
        print(green('Thanks!'))
    else:
        abort(red("Sorry, that's incorrect."))


def get_current_status():
    env.last_known_good = None
    env.has_current = False

    if files.exists(env.current):
        env.has_current = True
        with cd(env.current), hide('everything'):
            env.last_known_good = run('pwd -P')


def set_db_envs():
    func = local_python
    if env.is_remote:
        func = pyrun
    db = eval(
        func(("from django.conf import settings;print "
              "settings.DATABASES['default']")))
    env.db_password = db['PASSWORD']
    env.db_host = db['HOST']
    env.db_user = db['USER']
    env.db_name = db['NAME']


def set_remote_tempfile(suffix=None):
    if suffix:
        suffix = "suffix='{}'".format(suffix)
    else:
        suffix = ''
    py_cmd = 'import tempfile;print(tempfile.mkstemp({}))[1]'.format(suffix)
    env.tempfile = pyrun(py_cmd).strip()
