#usr/bin/python

import os
import sys

path_project='/home/home/simplecomment'
path_app='/home/home/simplecomment/sphinx_django'

if path_project not in sys.path:
    sys.path.append(path_project)

if path_app not in sys.path:
    sys.path.append(path_app)


print >> sys.stderr,str(sys.path)

import django.core.handlers.wsgi


os.environ['DJANGO_SETTINGS_MODULE'] = 'sphinx_django.settings'

_application = django.core.handlers.wsgi.WSGIHandler()


def application(environ, start_response):
    environ['PATH_INFO'] = environ['SCRIPT_NAME'] + environ['PATH_INFO']
    environ['SCRIPT_NAME'] = '' 
    return _application(environ, start_response)

