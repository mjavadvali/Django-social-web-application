from .base import *
import os

DEBUG = False


ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1", 'asgiserver']

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
MEDIA_URL = 'http://localhost/media/'
REDIS_URL = 'redis://cache:6379'
CACHES['default']['LOCATION'] = REDIS_URL
CHANNEL_LAYERS['default']['CONFIG']['hosts'] = [REDIS_URL]