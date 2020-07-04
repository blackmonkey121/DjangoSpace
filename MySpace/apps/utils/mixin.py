#!usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Monkey"

from django.shortcuts import render
from .tools import get_context


class NavViewMixin(object):
    """
    继承此类，默默的实现 navbar 所有信息 ，前提是对象必须在执行流程中调用`get_context_data` 方法,否则无效。
    对于不执行 `get_context_data`的情况（直接继承 View,甚至直接继承 Object 的）可以使用 `rich_render` 方法渲染。
    """

    def get_context_data(self, *args, **kwargs) -> dict:
        context = dict() if not hasattr(super(), 'get_context_data') else super().get_context_data(*args, **kwargs)

        context.update(
            get_context()
        )

        return context


def rich_render(*args, **kwargs) -> render:
    """ 仅仅是将 render 方法套个壳，添加导航栏上下文数据 """
    context = kwargs.get('context', None)
    if context is None:
        kwargs['context'] = context = dict()
    context.update(get_context())
    return render(*args, **kwargs)


# class CleanCacheMixin(object):
#
#     def save(self, *args, **kwargs):
#         """ 更新缓存 """
#         CacheMap.delete(model=self.__class__)
#         # cache_key = 'context:%s:list' % self.__class__.__name__.lower()
#         # cache.delete(cache_key)
#         super().save(*args, **kwargs)