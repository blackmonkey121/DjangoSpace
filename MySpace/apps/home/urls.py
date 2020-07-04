#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"


from django.urls import path
from .views import HomeView, AboutMe

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('me', AboutMe.as_view(), name='me'),
]
