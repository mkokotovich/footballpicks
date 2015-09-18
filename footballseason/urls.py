from django.conf.urls import url

from . import views

urlpatterns = [
    # eg: /footballseason/
    url(r'^$', views.index, name='index'),

    # eg: /footballseason/3
    url(r'^(?P<week_id>[0-9]+)/$', views.display, name='display'),

    # eg: /footballseason/3/submit
    url(r'^(?P<week_id>[0-9]+)/submit$', views.submit, name='submit'),

    # eg: /footballseason/3/vote
    url(r'^(?P<week_id>[0-9]+)/vote$', views.vote, name='vote'),
]
