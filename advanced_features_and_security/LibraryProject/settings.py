# Add at the top of the file
import os

# Update the AUTH_USER_MODEL setting
AUTH_USER_MODEL = 'relationship_app.CustomUser'

# Add media settings for profile photos
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
