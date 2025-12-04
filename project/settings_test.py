# Test-specific settings
from .settings import *

# Use SQLite in-memory database for tests
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Disable password validation to speed up tests
AUTH_PASSWORD_VALIDATORS = []
