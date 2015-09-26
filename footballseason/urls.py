from django.conf.urls import url

from . import views

urlpatterns = [
    # eg: /footballseason/
    url(r'^$', views.index, name='index'),

    # eg: /footballseason/3/
    url(r'^(?P<week_id>[0-9]+)/$', views.display, name='display'),

    # eg: /footballseason/3/submit/
    url(r'^(?P<week_id>[0-9]+)/submit/$', views.submit, name='submit'),

    # eg: /footballseason/3/vote/
    url(r'^(?P<week_id>[0-9]+)/vote/$', views.vote, name='vote'),

    # eg: /footballseason/update/
    url(r'^update/$', views.update, name='update'),

    # eg: /footballseason/records/
    url(r'^records/$', views.records_default, name='records_default'),

    # eg: /footballseason/records/2015/
    url(r'^records/(?P<season>[0-9]+)/$', views.records_by_season, name='records_by_season'),

    # eg: /footballseason/records/2015/3/
    url(r'^records/(?P<season>[0-9]+)/(?P<week>[0-9]+)/$', views.records_by_week, name='records_by_week'),
]
