from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-dd1#4676h=_0l^bp-3o48e@kw+tvs0)-x@*n2uty06%^bhfe61'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'shoplit',
#         'USER': 'postgres',  
#         'PASSWORD': os.getenv('DATABASE_PASSWORD'),  
#         'HOST': '127.0.0.1',
#         'PORT': '5432',  
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # this creates db.sqlite3 in your project root
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
    'redis': {
        'host': '127.0.0.1',
        'port': 6379,
        'db': 0, },
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

REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
     'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_THROTTLE_CLASSES': [],
    'DEFAULT_THROTTLE_RATES': {
        'user': None,  # disables user throttle
        'anon': None,
    }
}
