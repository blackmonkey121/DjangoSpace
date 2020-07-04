#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from dal import autocomplete

from apps.article.models import Category, Tag
from apps.travel.models import Province


class CategoryAutoComplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = Category.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class TagAutoComplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):

        qs = Tag.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class ProvinceComplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):

        qs = Province.objects.values('id', 'name').filter(status=Province.STATUS_NORMAL)
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
