from os.path import abspath, dirname, join

from fabric.api import env


env.template_dir = join(dirname(abspath(__file__)), 'templates')
