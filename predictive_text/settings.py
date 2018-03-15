import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'l+38ezh8br+y8_-#iphf7xv4a5rzg&wl$5%5p27c*lk6@0m-xo'

DEBUG = True

ALLOWED_HOSTS = ['jeffy.me', 'localhost', '127.0.0.1']

CORS_ORIGIN_ALLOW_ALL = True

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'corsheaders',
    'django_crontab',
    'rest_framework',
    'resource_collector',
    'predictive',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'predictive.utils.PageNumberPaginationExt',
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
    'PAGE_SIZE': 10,
}

ROOT_URLCONF = 'predictive_text.urls'

WSGI_APPLICATION = 'predictive_text.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'predictive_text',
        'USER': 'root',
        'PASSWORD': 'root123456',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "KEY_PREFIX": "django.predictive_text.caches",
        "TIMEOUT": 60 * 60 * 24,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PICKLE_VERSION": -1,
        }
    }
}

CRONJOBS = [
    (
        '0 0 * * *',
        'django.core.management.call_command',
        ['crawl_todays_article'],
        {},
        '>> %s/tmp/cronjobs/crawl_todays_article.log' % BASE_DIR,
    ),
    (
        '0 1 * * *',
        'django.core.management.call_command',
        ['analyze_articles'],
        {},
        '>> %s/tmp/cronjobs/analyze_articles.log' % BASE_DIR,
    ),
]

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False
