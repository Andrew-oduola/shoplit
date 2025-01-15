from .common import *
import os
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SECRET_KEY = os.environ('SECRET_KEY')
DATABASE_URL = os.environ('DATABASE_URL')

REDIS_URL = os.environ('REDISCLOUD_URL')
ALLOWED_HOSTS = ['shoplit-prod.herokuapp.com']

DATABASES = {
    'default': dj_database_url.config(DATABASE_URL)
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "TIMEOUT": 10 * 60,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
     }
}

Q_CLUSTER = {
    'name': 'shoplit',
    'workers': 8,
    'recycle': 500,
    'timeout': 60,
    'compress': True,
    'save_limit': 250,
    'queue_limit': 500,
    'cpu_affinity': 1,
    'label': 'Django Q2',
    'redis': REDIS_URL,
    'ALT_CLUSTERS': {
        'long': {
            'timeout': 3000,
            'retry': 3600,
            'max_attempts': 2,
        },
        'short': {
            'timeout': 10,
            'max_attempts': 1,
        },
    }
}

EMAIL_HOST = os.environ('MAILGUN_SMTP_SERVER')
EMAIL_HOST_USER = os.environ('MAILGUN_SMTP_LOGIN')
EMAIL_HOST_PASSWORD = os.environ('MAILGUN_SMTP_PASSWORD')
EMAIL_PORT = os.environ('MAILGUN_SMTP_PORT')