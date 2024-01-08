from .base import *

env = environ.Env()
environ.Env.read_env('.env')

DEBUG = False
ALLOWED_HOSTS += ['www.mogdynamics.com', 'mogdynamics.com', '138.68.166.64']

CSRF_TRUSTED_ORIGINS = [
    'https://mogdynamics.com',
    'https://www.mogdynamics.com'
]

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("DATABASE_NAME"),
        "USER": os.environ.get("DATABASE_USER"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD"),
        "HOST": os.environ.get("DATABASE_HOST", "localhost"),
        "PORT": os.environ.get("DATABASE_PORT")
    }
}

# Logging for production
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },

    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },

    "root": {
        "level": "INFO",
        "handlers": ["console"]
    },

    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': True,
        },
    },
}
