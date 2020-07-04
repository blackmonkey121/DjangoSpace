#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from dal import autocomplete
from django import forms
from mdeditor.fields import MDTextFormField

from .models import Article, Category, Tag


class ArticleAdminForm(forms.ModelForm):

    desc = forms.CharField(widget=forms.Textarea(attrs={'style': 'height: 100px;width:100%'}), label='摘要', required=False)

    content = MDTextFormField(label='正文', required=False)

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=autocomplete.ModelSelect2(url='category-autocomplete'),
        label='分类',
    )

    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='tag-autocomplete'),
        label='标签'

    )

    class Meta:
        model = Article
        fields = (
            'category', 'tag', 'desc', 'title',
            'content', 'status', 'visit',
        )