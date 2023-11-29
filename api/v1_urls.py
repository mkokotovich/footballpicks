from django.urls import re_path, include
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from api import v1_views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r"games", v1_views.GameViewSet)
router.register(r"teams", v1_views.TeamViewSet)
router.register(r"picks", v1_views.PickViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    re_path(r"^auth/", obtain_jwt_token),
    re_path(r"^records/$", v1_views.RecordsView.as_view()),
    re_path(r"^update/$", v1_views.RecordsUpdateView.as_view()),
    re_path(r"^update/records$", v1_views.RecordsUpdateView.as_view()),
    re_path(r"^update/schedule$", v1_views.ScheduleUpdateView.as_view()),
    re_path(r"^", include(router.urls)),
]
