#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"


from django.urls import path
from .views import AlbumView, ImageView

urlpatterns = [
    path('', AlbumView.as_view(), name='album'),
    path('', ImageView.as_view(), name='image'),
]
