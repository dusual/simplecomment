from django.conf.urls.defaults import *
from django.contrib import admin
from local_settings import *

import os
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()




urlpatterns = patterns('',
    # Example:
    # (r'^sphinx_django/', include('sphinx_django.foo.urls')),

    (r'^test/','sphinxcomment.views.test' ),
    (r'^chapter/', 'sphinxcomment.views.chapter'),
    (r'^count/(?P<chapter_name>.+)?$', 'sphinxcomment.views.chapter_count'),                  
    (r'^single/(?P<paragraph_id>[^/]+)/$', 'sphinxcomment.views.single'),
    (r'^submit/(?P<paragraph_id>[^/]+)/$', 'sphinxcomment.views.submit'),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     (r'^admin/', include(admin.site.urls)),
     (r'^pages/_static/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': os.path.join(PATH_STATIC_FILES,'static')}),
                    
     (r'^pages/(?P<path>.*)$', 'sphinxcomment.views.page'),
)
