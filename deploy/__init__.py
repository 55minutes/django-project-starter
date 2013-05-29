from os.path import abspath, dirname, join
import sys


PACKAGE_ROOT = dirname(dirname(abspath(__file__)))
PROJECT_ROOT = join(PACKAGE_ROOT, '{{ project_name }}')
VIRTUAL_ENV = abspath(sys.prefix)
