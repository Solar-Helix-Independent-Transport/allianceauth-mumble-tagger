from django.conf import settings
import re

def mumble_active():
    return 'allianceauth.services.modules.mumble' in settings.INSTALLED_APPS

