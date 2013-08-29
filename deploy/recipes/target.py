from os import environ
from os.path import abspath, dirname, join
import sys

from django.utils.crypto import get_random_string

from fabric.api import env, task


# Defaults, override at each target as necessary
env.db_user = env.name
env.is_remote = True  # Assume we're dealing with a remote host


@task
def local():
    "Set the deployment target to local."
    env.target = 'local'
    env.is_remote = False
    env.virtual_env = abspath(sys.prefix)
    env.package_root = abspath(join(dirname(__file__), '../..'))
    env.project_root = join(env.package_root, env.name)
    env.settings_fp = join(env.project_root, 'settings.py')
    env.static_root = join(env.project_root, 'static')
    env.guard_fp = join(env.package_root, 'Guardfile')
    env.gemset_fp = join(env.package_root, '.ruby-gemset')
    env.secret_key = get_random_string(54)
    env.db_user = environ['USER']
    env.db_password = ''
