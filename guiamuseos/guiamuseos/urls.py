"""guiamuseos URL Configuration

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
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from museos import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import login, logout

admin.autodiscover ()

urlpatterns = [
    url(r'^$', views.main, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login',  views.auth_login),
    url(r'^museos',  views.allmuseums),
    url(r'^logout', logout, {'next_page': '/'}),
    url(r'^register', views.register),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
