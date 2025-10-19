import os
import sys

path = '/home/yourusername/Alx_DjangoLearnLab/social_media_api'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'social_media_api.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()