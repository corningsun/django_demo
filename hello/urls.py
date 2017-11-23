#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf.urls import url

from hello import views

urlpatterns = (
    url(r'^hello/(?P<name>\w+)/$', views.Hello.as_view()),
)