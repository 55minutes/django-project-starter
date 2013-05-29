from base import *
from os.path import join

########## TEST SETTINGS
TEST_RUNNER = 'discover_runner.DiscoverRunner'
TEST_DISCOVER_TOP_LEVEL = PACKAGE_ROOT
TEST_DISCOVER_ROOT = join(PACKAGE_ROOT, 'tests')
TEST_DISCOVER_PATTERN = "test_*.py"
########## IN-MEMORY TEST DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}
