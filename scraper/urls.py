from django.conf.urls import patterns, url

from scraper import views

urlpatterns = patterns('',
	url(r'^$', views.search, name='search'),
	url(r'^hardware/(?P<pk>\d+)/$', views.HardwareView.as_view(), name='hardware'),
	url(r'^computer/(?P<pk>\d+)/$', views.ComputerView.as_view(), name='computer'),
)