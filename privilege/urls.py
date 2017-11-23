#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/9 上午10:12
# @Author  : OD
# @File    : urls.py
from privilege import views
from django.conf.urls import url

urlpatterns = (
    url(r'^privilege/login/$', views.Login.as_view()),
)