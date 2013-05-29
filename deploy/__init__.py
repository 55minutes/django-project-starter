from os.path import abspath, dirname, join

PACKAGE_ROOT = dirname(dirname(abspath(__file__)))
PROJECT_ROOT = join(PACKAGE_ROOT, '{{ project_name }}')
