from django.conf.urls import url

from . import views

urlpatterns = [
    # eg: /footballseason/
    url(r'^$', views.index, name='index'),

    # eg: /footballseason/3/display/
    url(r'^(?P<week_id>[0-9]+)/display/$', views.display, name='display'),

    # eg: /footballseason/3/submit/
    url(r'^(?P<week_id>[0-9]+)/submit/$', views.submit, name='submit'),

    # eg: /footballseason/3/vote/
    url(r'^(?P<week_id>[0-9]+)/vote/$', views.vote, name='vote'),

    # eg: /footballseason/submit
    url(r'^submit/$', views.submit, {'week_id': 0}, name='submit_current'),

    # eg: /footballseason/display
    url(r'^display/$', views.display, {'week_id': 0}, name='display_current'),

    # eg: /footballseason/live/
    url(r'^live/$', views.live, name='live'),

    # Hidden, for now
    # eg: /footballseason/update/
    url(r'^update/$', views.update, name='update'),

    # eg: /footballseason/records/
    url(r'^records/$', views.records, {'week': 1337, 'season':1337}, name='records_default'),

    # eg: /footballseason/records/2015/
    url(r'^records/(?P<season>[0-9]+)/$', views.records, {'week':0}, name='records_by_season'),

    # eg: /footballseason/records/2015/3/
    url(r'^records/(?P<season>[0-9]+)/(?P<week>[0-9]+)/$', views.records, name='records_by_week'),

]
