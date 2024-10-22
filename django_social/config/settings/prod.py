from .base import *
import os

DEBUG = False


ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1", 'asgiserver2', '0.0.0.0:9000']

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "postgres"),  
        "USER": os.environ.get("POSTGRES_USER", "postgres"),  
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
        "HOST": 'db', 
        "PORT": '5432', 
    }
}
REDIS_URL = 'redis://cache:6379'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [REDIS_URL], 
        },
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': REDIS_URL, 
    }
}
MEDIA_URL = 'http://localhost/media/'
STATIC_URL = "http://localhost/staticfiles/"