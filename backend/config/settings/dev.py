import os

from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

if os.getenv("DEV_DB", "sqlite").lower() == "sqlite":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = (
    "rest_framework.permissions.AllowAny",
)