from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
   # Example:
   # (r'^sec/', include('sec.foo.urls')),

   # Uncomment the admin/doc line below to enable admin documentation:
   #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

   # Uncomment the next line to enable the admin:
	(r'^admin/', include(admin.site.urls)),

	(r'^stats/', 'stats.views.index'),
	(r'^$', 'signin.views.index'),
	(r'^signin/', 'signin.views.signin'),
	(r'^new/', 'signin.views.createNewRecord'),
	(r'^addorg/(?P<trimmed_idnum>\d+)/$', 'signin.views.addOrganization'),
	(r'^createorg/$', 'signin.views.createNewOrganization'),
)
