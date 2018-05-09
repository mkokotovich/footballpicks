from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from api import v1_views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'games', v1_views.GameViewSet)
router.register(r'teams', v1_views.TeamViewSet)
router.register(r'picks', v1_views.PickViewSet)
router.register(r'records', v1_views.RecordViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    url(r'^', include(router.urls))
]
