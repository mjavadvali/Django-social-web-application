from .base import *
import os
from dotenv import load_dotenv


DEBUG = False

load_dotenv(os.path.join(BASE_DIR, 'envs/.env'))
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1", 'asgiserver2', '0.0.0.0:9000']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('PGDB_NAME'),
        'USER': os.getenv('PGDB_USER'),
        'PASSWORD': os.getenv('PGDB_PASSWORD'),
        'HOST': os.getenv('PGDB_HOST', 'db'),
        'PORT': os.getenv('PGDB_PORT', '5432'),
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