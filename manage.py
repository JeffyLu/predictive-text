#coding:utf-8

import os
import sys
import django
from django.conf import settings


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORDS_PATH = os.path.join(BASE_DIR, 'data', 'words.txt')
VOA_DIR = os.path.join(BASE_DIR, 'data', 'VOA')

INSTALLED_APPS = [
    'db',
]


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


DATABASES = {
    'default': {
        'ENGINE' : 'django.db.backends.mysql',
        'NAME' : 'test',
        'USER' : 'root',
        'PASSWORD' : 'root',
        'HOST' : 'localhost',
        'PORT' : '3306',
        'OPTIONS': {
           'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
       }
    }
}

settings.configure(
    INSTALLED_APPS = INSTALLED_APPS,
    DATABASES = DATABASES,
)

django.setup()

if __name__ == "__main__":
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
