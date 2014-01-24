from django.conf.urls import patterns, include, url
from django.views.generic.simple import redirect_to

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^', redirect_to, {'url': '/search/'}),
    url(r'^search/', include('scraper.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
