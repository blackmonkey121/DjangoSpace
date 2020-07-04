#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from django.db import models
from .tools import CacheMap

class BaseModel(models.Model):

    STATUS_DRAFT = 2
    STATUS_NORMAL = 1
    STATUS_DELETE = 0

    STATUS_ITEMS = (
        (STATUS_NORMAL, '发布'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '待发布'),
    )

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")

    def save(self, *args, **kwargs):

        CacheMap.delete(model=self.__class__)

        super(BaseModel, self).save(*args, **kwargs)

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