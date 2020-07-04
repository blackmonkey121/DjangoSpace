#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"


from django.urls import path
from .views import ArticleListView, ArticleDetailView, CategoryListView, TagListView, ArchiveListView

urlpatterns = [
    path('', ArticleListView.as_view(), name="article"),
    path('<int:id>/', ArticleDetailView.as_view(), name="detail"),
    path('tag/<int:id>', TagListView.as_view(), name="tag"),
    path('category/<int:id>', CategoryListView.as_view(), name="category"),
    path('archive/<int:year>/<int:month>', ArchiveListView.as_view(), name="archive"),

]
