"""
WSGI config for Atmosphere project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys
import site


PROJECT_DIR = '/var/www/html/django_app/Atmosphere'
if os.path.exists(PROJECT_DIR):
    PACKAGE_DIR = os.path.join(PROJECT_DIR, '/usr/local/lib/python3.6/dist-packages')

    sys.stdout = sys.stderr

# os.environ["DJANGO_SETTINGS_MODULE"] = "Atmosphere.settings"
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Atmosphere.settings")

if os.path.exists(PROJECT_DIR):
    sys.path.insert(0, PROJECT_DIR)
    sys.path.insert(1, PACKAGE_DIR)
    site.addsitedir(PACKAGE_DIR)


from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
