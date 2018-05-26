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
from django.conf.urls import url
from django.urls import include
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

urlpatterns = [
    url(r'^footballseason/', include('footballseason.urls')),
    url(r'^old/', include('footballseason.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='footballseason/login.html'), name="login"),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name="logout"),
    url(r'^api/v1/', include('api.v1_urls')),
    url(r'^', include('footballseason.urls')),
]
