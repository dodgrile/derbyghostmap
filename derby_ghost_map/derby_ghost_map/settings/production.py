from .base import *

DEBUG = False

try:
    from .local import *
except ImportError:
    pass

from .base import *
import os
import dj_database_url

DEBUG = False

# Fetch secret key from environment variable
SECRET_KEY = os.environ.get('SECRET_KEY')

# Allow all hosts or specify your Render domain
ALLOWED_HOSTS = ['*']  # or ['your-app-name.onrender.com']

# Configure the database using Render's database URL
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}

# Use WhiteNoise for static files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True