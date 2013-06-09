# Generated by Fabric
# vars: $$target, $$db_password, $$secret_key, $$static_root, $$postmark_api_key

from ${name}.config.${target} import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'NAME': '${name}_${target}',
        'USER': '${db_user}',
        'PASSWORD': '${db_password}',
    },
}
SECRET_KEY = '${secret_key}'
STATIC_ROOT = '${static_root}'
POSTMARK_API_KEY = '${postmark_api_key}'
