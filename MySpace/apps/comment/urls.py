#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"


from django.urls import path
from .views import ArticleCommentView

urlpatterns = [
    path('article/<int:article_id>/', ArticleCommentView.as_view(), name="comment"),
]
