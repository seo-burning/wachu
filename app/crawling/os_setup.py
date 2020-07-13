
import sys
import os
import django
PROJECT_ROOT = os.getcwd()
sys.path.append(PROJECT_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings.prod")
django.setup()
