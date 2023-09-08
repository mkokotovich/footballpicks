from django.urls import re_path

from . import views

urlpatterns = [
    # eg: /footballseason/
    re_path(r"^$", views.index, name="index"),
    # eg: /footballseason/display/2015/3/
    re_path(r"^display/(?P<season_id>[0-9]+)/(?P<week_id>[0-9]+)/$", views.display, name="display"),
    # eg: /footballseason/submit/2015/3
    re_path(r"^submit/(?P<season_id>[0-9]+)/(?P<week_id>[0-9]+)/$", views.submit, name="submit"),
    # eg: /footballseason/vote/2015/3
    re_path(r"^vote/(?P<season_id>[0-9]+)/(?P<week_id>[0-9]+)/$", views.vote, name="vote"),
    # eg: /footballseason/submit/2015
    re_path(r"^submit/(?P<season_id>[0-9]+)$", views.submit, {"week_id": 0}, name="submit_season"),
    # eg: /footballseason/display/2015
    re_path(r"^display/(?P<season_id>[0-9]+)/$", views.display, {"week_id": 0}, name="display_season"),
    # eg: /footballseason/submit/
    re_path(r"^submit/$", views.submit, {"season_id": 0, "week_id": 0}, name="submit_current"),
    # eg: /footballseason/display/
    re_path(r"^display/$", views.display, {"season_id": 0, "week_id": 0}, name="display_current"),
    # eg: /footballseason/live/
    re_path(r"^live/$", views.live, name="live"),
    # Hidden, for now
    # eg: /footballseason/update/
    re_path(r"^update/$", views.update, name="update"),
    # eg: /footballseason/records/
    re_path(r"^records/$", views.records, {"view": "week"}, name="records_default"),
    # eg: /footballseason/records/2015/
    re_path(
        r"^records/(?P<season_id>[0-9]+)/$", views.records, {"week": 0, "view": "season"}, name="records_by_season"
    ),
    # eg: /footballseason/records/2015/3/
    re_path(
        r"^records/(?P<season_id>[0-9]+)/(?P<week>[0-9]+)/$", views.records, {"view": "week"}, name="records_by_week"
    ),
    # eg: /footballseason/records/2015/month/9/
    re_path(
        r"^records/(?P<season_id>[0-9]+)/month/(?P<month>[0-9]+)/$",
        views.records,
        {"view": "month"},
        name="records_by_month",
    ),
    # eg: /footballseason/records/alltime/
    re_path(r"^records/alltime/$", views.records, {"view": "alltime"}, name="records_all_time"),
]
