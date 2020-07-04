#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.article.models import Article


class ArticleSitemap(Sitemap):
    changefreq = "always"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Article.objects.filter(status=Article.STATUS_NORMAL)

    def lastmod(self, obj):
        return obj.create_time

    def location(self, obj):
        return reverse('article:detail', args=[obj.pk])

