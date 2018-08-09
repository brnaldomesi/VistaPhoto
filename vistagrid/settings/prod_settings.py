from vistagrid.settings.base_settings import *

DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES['default'] = dj_database_url.config()