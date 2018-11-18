"""ig_scheduler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from igs.views import *
from rest_framework.authtoken import views as rest_framework_views
# from django.urls import path
from igs.views import login
# import rest_framework

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^user/$', UserDetail.as_view()),
    # url(r'^api/login/',rest_framework.urls),
    url('api/login', login),
    url(r'^api/searchimage', imagesearch),
    url(r'^get_auth_token/$', rest_framework_views.obtain_auth_token, name='get_auth_token'),

]
