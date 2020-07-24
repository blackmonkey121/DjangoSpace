#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from django.core.cache import cache
from django.db import models
from django.db.models import Manager


class BaseManager(Manager):

    def get_abstract_all(self):
        return super(BaseManager, self).all()

    def filter(self, *args, **kwargs):
        return super(BaseManager, self).filter(status=self.model.STATUS_NORMAL, *args, **kwargs)

    def all(self):
        return super(BaseManager, self).filter(status=self.model.STATUS_NORMAL)


class BaseModel(models.Model):

    STATUS_DRAFT: int = 2
    STATUS_NORMAL: int = 1
    STATUS_DELETE: int = 0

    STATUS_ITEMS: (tuple, list) = (
        (STATUS_NORMAL, '发布'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '待发布'),
    )

    CACHE_DICT: dict = {
        'keys': None,
        'match': None,
    }

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    objects = BaseManager()

    def flush_cache_keys(self) -> dict:
        """
        返回需要刷新的缓存字典 dict{"keys":'Iterable', "match":'Iterable'}
        "keys": 刷新的键
        "match": 通配符匹配键
        @return: dict{"keys":[...], "match":[...]}
        """
        return self.CACHE_DICT

    def save(self, *args, **kwargs) -> None:

        super(BaseModel, self).save(*args, **kwargs)
        cache_dict: dict = self.flush_cache_keys() or self.CACHE_DICT

        if cache_dict['keys']:
            [cache.delete(key) for key in cache_dict['keys']]
        if cache_dict['match']:
            [cache.delete(key) for key in [cache.iter_keys(key) for key in cache_dict['match']]]

    class Meta:
        abstract = True
        ordering = ['-id']


class VisitBaseModel(BaseModel):

    visit = models.IntegerField(default=0, verbose_name='浏览量')

    class Meta:
        abstract = True


class FileManager(VisitBaseModel):
    desc = models.CharField(max_length=256, verbose_name='描述')

    class Meta:
        abstract = True