#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"


from django.urls import path
from .views import AlbumListView, ImageView, AlbumDetailView

urlpatterns = [
    path('', AlbumListView.as_view(), name='album'),
    path('album/<int:id>', AlbumDetailView.as_view(), name='album_detail'),
    path('album/<int:album_id>/image/<int:image_id>', ImageView.as_view(), name='image_detail'),
]
