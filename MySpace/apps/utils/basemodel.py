#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from django.db import models

from ..utils.mixin import FlushCacheMixin


class BaseModel(FlushCacheMixin, models.Model):

    STATUS_DRAFT: int = 2
    STATUS_NORMAL: int = 1
    STATUS_DELETE: int = 0

    STATUS_ITEMS: (tuple, list) = (
        (STATUS_NORMAL, '发布'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '待发布'),
    )

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")

    class Meta:
        abstract = True


class VisitBaseModel(BaseModel):

    visit = models.SmallIntegerField(default=0, verbose_name='浏览量')

    class Meta:
        abstract = True


class FileManager(VisitBaseModel):
    desc = models.CharField(max_length=256, verbose_name='描述')

    class Meta:
        abstract = True