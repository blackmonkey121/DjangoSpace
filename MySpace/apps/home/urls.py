#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"


from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('me', AboutMe.as_view(), name='me'),
    path('search', AllSiteSearch.as_view(), name='search'),
]
