"""footballpicks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.urls import include, path
from django.views.generic.base import RedirectView
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(r'footballseason/login/', auth_views.LoginView.as_view(template_name='footballseason/login.html'), name="login"),
    path(r'footballseason/logout/', auth_views.LogoutView.as_view(), {'next_page': '/footballseason/'}, name="logout"),
    path(r'footballseason/', include('footballseason.urls')),
    path(r'old/', RedirectView.as_view(url='/footballseason/', permanent=False), name='footballseason'),
    path(r'admin/', admin.site.urls),
    path(r'api/v1/', include('api.v1_urls')),
]
