# Add at the top of the file
import os

# Update the AUTH_USER_MODEL setting
AUTH_USER_MODEL = 'bookshelf.Customer'

INSTALLED_APPS = [
    'bookshelf',  # This should come first
    'relationship_app',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Add media settings for profile photos
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
