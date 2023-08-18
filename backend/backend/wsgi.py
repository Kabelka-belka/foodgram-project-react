import os, sys

from django.core.wsgi import get_wsgi_application


sys.path.append('/var/www/foodgram-project-react/backend')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_wsgi_application()
