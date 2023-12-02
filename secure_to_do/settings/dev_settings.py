from .base_Settings import *


DEBUG = env.bool("DEBUG", True)

# noqa
INSTALLED_APPS = INSTALLED_APPS + ["django_extensions"]
ALLOWED_HOSTS = ['localhost']