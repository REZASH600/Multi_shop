import os

from .base import *

SECRET_KEY = os.environ.get("SECRET_KEY", 'django-insecure-@$t6djrqsbbgg5em3gzp#j!uudo5*dw0t#amdm(7q#7j)#9##_')

DEBUG = bool(os.environ.get("DEBUG", default=0))

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split()

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", path.join(BASE_DIR, 'volumes', 'db', 'db.sqlite3')),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}
