from .base import *

env = environ.Env()
environ.Env.read_env('.env')

DEBUG = True

ALLOWED_HOSTS += ['localhost', '127.0.0.1']

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


# Logging for development

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'my_log_handler': {
#             'level': 'DEBUG' if DEBUG else 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': os.path.join(BASE_DIR, 'logs/debug.log'),
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['my_log_handler'],
#             'level': 'DEBUG' if DEBUG else 'INFO',
#             'propagate': True,
#         },
#     },
# }
