from os.path import abspath, dirname, join
import sys

from django.utils.crypto import get_random_string

from fabric.api import env, task


env.project_name = '{{ project_name }}'


@task
def local():
    "Set the deployment target to local."
    env.target = 'local'
    env.virtual_env = abspath(sys.prefix)
    env.package_root = dirname(dirname(abspath(__file__)))
    env.project_root = join(env.package_root, '{{ project_name }}')
    env.settings_fp = join(env.project_root, 'settings.py')
    env.static_root = join(env.project_root, 'assets')
    env.secret_key = get_random_string(54)
    env.db_password = ''