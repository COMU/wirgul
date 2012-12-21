import os, sys

project_path = "/home/oguz/"
project_app_path = "/home/oguz/wirgul"

if project_path not in sys.path:
    sys.path.append(project_path)
if project_app_path not in sys.path:
    sys.path.append(project_app_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'wirgul.settings'

import django.core.handlers.wsgi

_application = django.core.handlers.wsgi.WSGIHandler()

def application(environ, start_response):
    environ['PATH_INFO'] = environ['SCRIPT_NAME'] + environ['PATH_INFO']
    return _application(environ, start_response)
