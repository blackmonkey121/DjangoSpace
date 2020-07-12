#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from django.forms import forms
from mdeditor.fields import MDTextFormField

class ArticleCommentForm(forms.Form):
    # context = MDTextFormField(label='支持MarkDown！', widget={})
    context = MDTextFormField(label='支持MarkDown！')