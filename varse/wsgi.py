
import os
from django.core.wsgi import get_wsgi_application

# ✅ Ensure this matches your folder name exactly
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'varse.settings')

application = get_wsgi_application()


