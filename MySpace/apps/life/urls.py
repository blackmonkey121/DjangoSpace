#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"


from django.urls import path
from .views import LifeView, CookingView, BookView, NoteView, PerceptionView

urlpatterns = [
    path('', LifeView.as_view(), name='life'),
    path('cooking/', CookingView.as_view(), name='cook_list'),
    path('book/', BookView.as_view(), name='book_list'),
    path('note/', NoteView.as_view(), name='note_list'),
    path('perception/', PerceptionView.as_view(), name='perception_list'),

    path('cooking/<int:id>', CookingView.as_view(), name='cook'),
    path('book/<int:id>', BookView.as_view(), name='book'),
    path('note/<int:id>', NoteView.as_view(), name='note'),
    path('perception/<int:id>', PerceptionView.as_view(), name='perception'),
]
